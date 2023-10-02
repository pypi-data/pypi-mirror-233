from collections.abc import Hashable
from typing import Literal, overload

import dask.array
import numpy as np
import xarray as xr

from xarray_regrid import utils


@overload
def interp_regrid(
    data: xr.DataArray,
    target_ds: xr.Dataset,
    method: Literal["linear", "nearest", "cubic"],
) -> xr.DataArray:
    ...


@overload
def interp_regrid(
    data: xr.Dataset,
    target_ds: xr.Dataset,
    method: Literal["linear", "nearest", "cubic"],
) -> xr.Dataset:
    ...


def interp_regrid(
    data: xr.DataArray | xr.Dataset,
    target_ds: xr.Dataset,
    method: Literal["linear", "nearest", "cubic"],
) -> xr.DataArray | xr.Dataset:
    """Refine a dataset using xarray's interp method.

    Args:
        data: Input dataset.
        target_ds: Dataset which coordinates the input dataset should be regrid to.
        method: Which interpolation method to use (e.g. 'linear', 'nearest').

    Returns:
        Regridded input dataset
    """
    coord_names = set(target_ds.coords).intersection(set(data.coords))
    coords = {name: target_ds[name] for name in coord_names}

    return data.interp(
        coords=coords,
        method=method,
    )


@overload
def conservative_regrid(
    data: xr.DataArray,
    target_ds: xr.Dataset,
    latitude_coord: str | None,
) -> xr.DataArray:
    ...


@overload
def conservative_regrid(
    data: xr.Dataset,
    target_ds: xr.Dataset,
    latitude_coord: str | None,
) -> xr.Dataset:
    ...


def conservative_regrid(
    data: xr.DataArray | xr.Dataset,
    target_ds: xr.Dataset,
    latitude_coord: str | None,
) -> xr.DataArray | xr.Dataset:
    """Refine a dataset using conservative regridding.

    The method implementation is based on a post by Stephan Hoyer; "For the case of
    interpolation between rectilinear grids (even on the sphere), you can factorize
    regridding along each axis. This is less general but makes the entire calculation
    much simpler, because its feasible to store interpolation weights as dense matrices
    and to use dense matrix multiplication."
    https://discourse.pangeo.io/t/conservative-region-aggregation-with-xarray-geopandas-and-sparse/2715/3

    Args:
        data: Input dataset.
        target_ds: Dataset which coordinates the input dataset should be regrid to.

    Returns:
        Regridded input dataset
    """
    if latitude_coord is not None:
        if latitude_coord not in data.coords:
            msg = "Latitude coord not in input data!"
            raise ValueError(msg)
    else:
        latitude_coord = ""

    dim_order = list(target_ds.dims)

    coord_names = set(target_ds.coords).intersection(set(data.coords))
    coords = {name: target_ds[name] for name in coord_names}
    data = data.sortby(list(coord_names))

    if isinstance(data, xr.Dataset):
        return conservative_regrid_dataset(data, coords, latitude_coord).transpose(
            *dim_order, ...
        )
    else:
        return conservative_regrid_dataarray(data, coords, latitude_coord).transpose(
            *dim_order, ...
        )


def conservative_regrid_dataset(
    data: xr.Dataset,
    coords: dict[Hashable, xr.DataArray],
    latitude_coord: str,
) -> xr.Dataset:
    """Dataset implementation of the conservative regridding method."""
    data_vars: list[str] = list(data.data_vars)
    dataarrays = [data[var] for var in data_vars]

    for coord in coords:
        target_coords = coords[coord].to_numpy()
        source_coords = data[coord].to_numpy()
        weights = get_weights(source_coords, target_coords)

        # Modify weights to correct for latitude distortion
        if str(coord) == latitude_coord:
            dot_array = utils.create_dot_dataarray(
                weights, str(coord), target_coords, source_coords
            )
            dot_array = apply_spherical_correction(dot_array, latitude_coord)
            weights = dot_array.to_numpy()

        for i in range(len(dataarrays)):
            if coord in dataarrays[i].coords:
                da = dataarrays[i].transpose(coord, ...)
                dataarrays[i] = apply_weights(da, weights, coord, target_coords)

    return xr.merge(dataarrays)  # TODO: add other coordinates/data variables back in.


def conservative_regrid_dataarray(
    data: xr.DataArray,
    coords: dict[Hashable, xr.DataArray],
    latitude_coord: str,
) -> xr.DataArray:
    """DataArray implementation of the conservative regridding method."""
    for coord in coords:
        if coord in data.coords:
            target_coords = coords[coord].to_numpy()
            source_coords = data[coord].to_numpy()

            weights = get_weights(source_coords, target_coords)

            # Modify weights to correct for latitude distortion
            if str(coord) == latitude_coord:
                dot_array = utils.create_dot_dataarray(
                    weights, str(coord), target_coords, source_coords
                )
                dot_array = apply_spherical_correction(dot_array, latitude_coord)
                weights = dot_array.to_numpy()

            data = data.transpose(coord, ...)
            data = apply_weights(data, weights, coord, target_coords)

    return data


def apply_weights(
    da: xr.DataArray, weights: np.ndarray, coord_name: Hashable, new_coords: np.ndarray
) -> xr.DataArray:
    """Apply the weights to convert data to the new coordinates."""
    if da.chunks is not None:
        # Dask routine
        new_data = dask.array.einsum(
            "i...,ij->j...", da.data, weights, optimize="greedy"
        )
    else:
        # numpy routine
        new_data = np.einsum("i...,ij->j...", da.data, weights)

    coord_mapping = {coord_name: new_coords}
    coords = list(da.dims)
    coords.remove(coord_name)
    for coord in coords:
        coord_mapping[coord] = da[coord].to_numpy()

    return xr.DataArray(
        data=new_data,
        coords=coord_mapping,
        name=da.name,
    )


def get_weights(source_coords: np.ndarray, target_coords: np.ndarray) -> np.ndarray:
    """Determine the weights to map from the old coordinates to the new coordinates.

    Args:
        source_coords: Source coordinates (center points)
        target_coords Target coordinates (center points)

    Returns:
        Weights, which can be used with a dot product to apply the conservative regrid.
    """
    # TODO: better resolution/IntervalIndex inference
    target_intervals = utils.to_intervalindex(
        target_coords, resolution=target_coords[1] - target_coords[0]
    )

    source_intervals = utils.to_intervalindex(
        source_coords, resolution=source_coords[1] - source_coords[0]
    )
    overlap = utils.overlap(source_intervals, target_intervals)
    return utils.normalize_overlap(overlap)


def apply_spherical_correction(
    dot_array: xr.DataArray, latitude_coord: str
) -> xr.DataArray:
    """Apply a sperical earth correction on the prepared dot product weights."""
    da = dot_array.copy()
    latitude_res = np.median(np.diff(dot_array[latitude_coord].to_numpy(), 1))
    lat_weights = lat_weight(dot_array[latitude_coord].to_numpy(), latitude_res)
    da.values = utils.normalize_overlap(dot_array.values * lat_weights[:, np.newaxis])
    return da


def lat_weight(latitude: np.ndarray, latitude_res: float) -> np.ndarray:
    """Return the weight of gridcells based on their latitude.

    Args:
        latitude: (Center) latitude values of the gridcells, in degrees.
        latitude_res: Resolution/width of the grid cells, in degrees.

    Returns:
        Weights, same shape as latitude input.
    """
    dlat: float = np.radians(latitude_res)
    lat = np.radians(latitude)
    h = np.sin(lat + dlat / 2) - np.sin(lat - dlat / 2)
    return h * dlat / (np.pi * 4)  # type: ignore
