#!/usr/bin/env python3
"""Viewer functions for Jupyter notebooks."""
import io
import pathlib
import uuid

import numpy as np

from ..atoms import Atoms
from ..data import COVALENT_RADII, CPK_COLORS
from ..io import create_pdb_str, read_cube, read_traj, read_xyz
from ..logger import log
from ..tools import get_isovalue
from .fods import split_fods


def view(*args, **kwargs):
    """Unified display function."""
    if isinstance(args[0], (str, list, tuple)):
        return view_file(*args, **kwargs)
    return view_atoms(*args, **kwargs)


def view_atoms(obj, extra=None, plot_n=False, percent=85, surfaces=20):
    """Display atoms with optional FODs or grid points, or even densities.

    Reference: https://plotly.com/python

    Args:
        obj: Atoms or SCF object.

    Keyword Args:
        extra (ndarray | list): Extra coordinates or FODs to display.
        plot_n (bool): Weather to plot the electronic density (only for executed scf objects).
        percent (float): Amount of density that should be contained.
        surfaces (int): Number of surfaces to display in density plots (reduce for performance).

    Returns:
        None.
    """
    try:
        import plotly.graph_objects as go
    except ImportError:
        log.exception('Necessary dependencies not found. To use this module, '
                      'install them with "pip install eminus[viewer]".\n\n')
        raise
    atoms = obj._atoms

    fig = go.Figure()
    # Add species one by one to be able to have them named and be selectable in the legend
    # Note: The size scaling is mostly arbitrary and has no meaning
    for ia in sorted(set(atoms.atom)):
        mask = np.where(np.asarray(atoms.atom) == ia)[0]
        atom_data = go.Scatter3d(x=atoms.pos[mask, 0], y=atoms.pos[mask, 1], z=atoms.pos[mask, 2],
                                 name=ia,
                                 mode='markers',
                                 marker={'size': 2 * np.pi * np.sqrt(COVALENT_RADII[ia]),
                                         'color': CPK_COLORS[ia],
                                         'line': {'color': 'black', 'width': 2}})
        fig.add_trace(atom_data)
    if extra is not None:
        # If a list has been provided with a length of two it has to be FODs
        if isinstance(extra, list):
            if len(extra[0]) != 0:
                extra_data = go.Scatter3d(x=extra[0][:, 0], y=extra[0][:, 1], z=extra[0][:, 2],
                                          name='up-FOD',
                                          mode='markers',
                                          marker={'size': np.pi, 'color': 'red'})
                fig.add_trace(extra_data)
            if len(extra) > 1 and len(extra[1]) != 0:
                extra_data = go.Scatter3d(x=extra[1][:, 0], y=extra[1][:, 1], z=extra[1][:, 2],
                                          name='down-FOD',
                                          mode='markers',
                                          marker={'size': np.pi, 'color': 'green'})
                fig.add_trace(extra_data)
        # Treat extra as normal coordinates otherwise
        else:
            extra_data = go.Scatter3d(x=extra[:, 0], y=extra[:, 1], z=extra[:, 2],
                                      name='Coordinates',
                                      mode='markers',
                                      marker={'size': 1, 'color': 'red'})
            fig.add_trace(extra_data)

    # A density can be plotted for an SCF object
    if isinstance(plot_n, np.ndarray) or plot_n:
        # Plot a given array or use the density from an SCF object
        if isinstance(plot_n, np.ndarray):
            density = plot_n
        else:
            density = obj.n
        den_data = go.Volume(x=atoms.r[:, 0], y=atoms.r[:, 1], z=atoms.r[:, 2], value=density,
                             name='Density',
                             colorbar_title=f'Density ({percent}%)',
                             colorscale='Inferno',
                             isomin=get_isovalue(density, percent=percent),
                             isomax=np.max(density),
                             surface_count=surfaces,
                             opacity=0.1,
                             showlegend=True)
        fig.add_trace(den_data)
        # Move colorbar to the left
        fig.data[-1].colorbar.x = -0.15

    # Theming
    scene = {'xaxis': {'title': 'x [a<sub>0</sub>]'},
             'yaxis': {'title': 'y [a<sub>0</sub>]'},
             'zaxis': {'title': 'z [a<sub>0</sub>]'},
             'aspectmode': 'cube'}
    # If the unit cell is diagonal and we scale the plot, otherwise let plotly decide
    if (np.diag(np.diag(atoms.a)) == atoms.a).all():
        scene['xaxis']['range'] = [0, atoms.a[0, 0]]
        scene['yaxis']['range'] = [0, atoms.a[1, 1]]
        scene['zaxis']['range'] = [0, atoms.a[2, 2]]
    fig.update_layout(scene=scene,
                      legend={'itemsizing': 'constant', 'title': 'Selection'},
                      hoverlabel_bgcolor='black',
                      template='none')
    fig.show()


def view_file(filename, isovalue=0.01, gui=False, elec_symbols=('X', 'He'),
              size=('400px', '400px'), **kwargs):
    """Display molecules and orbitals.

    Reference: Bioinformatics 34, 1241.

    Args:
        filename (str | list | tuple): Input filename(s). This can be either CUBE or XYZ files.

    Keyword Args:
        isovalue (float): Isovalue for sizing orbitals.
        gui (bool): Turn on the NGLView GUI.
        elec_symbols (list): Identifier for up and down FODs.
        size (tuple): Widget size.

    Keyword Args:
        **kwargs: NGLWidget keyword arguments.

    Returns:
        NGLWidget: Viewable object.
    """
    try:
        from nglview import NGLWidget, write_html
    except ImportError:
        log.exception('Necessary dependencies not found. To use this module, '
                      'install them with "pip install eminus[viewer]".\n\n')
        raise

    # If multiple files are given, try to open them with an interact drop-down menu
    # If all files are XYZ files they will be displayed as a trajectory instead
    if isinstance(filename, (list, tuple)) and not np.all([f.endswith('.xyz')for f in filename]):
        if executed_in_notebook():
            from ipywidgets import interact
            interact(lambda filename: view_file(filename, isovalue, gui, elec_symbols,
                                                **kwargs), filename=filename)
            return None
        # If we are not in a notebook open the files one by one
        for f in filename:
            view_file(f, isovalue, gui, elec_symbols, **kwargs)
            return None

    view = NGLWidget(**kwargs)
    view._set_size(*size)
    # Set the gui to the view
    if gui:
        view.gui_style = 'ngl'

    # Handle TRAJ files (or multiple XYZ files)
    if isinstance(filename, (list, tuple)) or filename.endswith(('.trj', '.traj')):
        view = _traj_view(view, filename)
    # Handle XYZ files
    elif filename.endswith('.xyz'):
        view = _xyz_view(view, filename, elec_symbols)
    # Handle CUBE files
    elif filename.endswith(('.cub', '.cube')):
        view = _cube_view(view, filename, isovalue, elec_symbols)
    # Handle other files (mainly for PDBs)
    else:
        view = _generic_view(view, filename)

    # Check if the function has been executed in a notebook
    # If yes, just return the view
    if executed_in_notebook():
        return view
    # Otherwise the viewer would display nothing
    # But if plotly is installed on can write the view to a StringIO object and display it with the
    # smart open_html_in_browser function from plotly that automatically opens a new browser tab
    try:
        from plotly.io._base_renderers import open_html_in_browser
        # Use StringIO object instead of a temporary file
        with io.StringIO() as html:
            write_html(html, view)
            open_html_in_browser(html.getvalue())
    except ImportError:
        log.error('This function only works in notebooks or with Plotly installed.')
    return None


def executed_in_notebook():
    """Check if the code runs in a notebook.

    Reference: https://stackoverflow.com/a/22424821

    Returns:
        bool: Weather in a notebook or not.
    """
    try:
        from IPython import get_ipython
        if 'IPKernelApp' not in get_ipython().config:
            return False
    except (AttributeError, ImportError):
        return False
    return True


def _generic_view(view, filename):
    """Modify the view for a generic (probably PDB) file.

    Args:
        view (NGLWidget): Viewable object.
        filename (str): Input filename.

    Returns:
        NGLWidget: Viewable object.
    """
    # If no XYZ or CUBE file is used try a more generic file viewer
    ext = pathlib.Path(filename).suffix.replace('.', '')
    # It seems that only PDB works with this method
    if ext != 'pdb':
        log.warning('Only XYZ, CUBE, and PDB files are support, but others might work.')
    with open(filename, 'r') as fh:
        view.add_component(fh, ext=ext)
    view[0].clear()
    view[0].add_ball_and_stick()
    view.center()
    return view


def _cube_view(view, filename, isovalue, elec_symbols):
    """Modify the view for a given CUBE file.

    Args:
        view (NGLWidget): Viewable object.
        filename (str | list | tuple): Input filename(s).
        isovalue (float): Isovalue for sizing orbitals.
        elec_symbols (list): Identifier for up and down FODs.

    Returns:
        NGLWidget: Viewable object.
    """
    from nglview import TextStructure
    # Atoms and cell
    atom, pos, _, a, _, _ = read_cube(filename)
    atom, pos, pos_fod = split_fods(atom, pos, elec_symbols)
    view.add_component(TextStructure(create_pdb_str(atom, pos, a)))
    view[0].clear()
    view[0].add_ball_and_stick()
    view.add_unitcell()
    view.center()
    # Spin up
    view.add_component(filename)
    view[1].clear()
    view[1].add_surface(negateIsolevel=False,
                        isolevelType='value',
                        isolevel=isovalue,
                        color='lightgreen',
                        opacity=0.75,
                        side='front',
                        depthWrite=False)
    # Spin down
    view.add_component(filename)
    view[2].clear()
    view[2].add_surface(negateIsolevel=True,
                        isolevelType='value',
                        isolevel=isovalue,
                        color='red',
                        opacity=0.75,
                        side='front',
                        depthWrite=False)
    # Spin up FODs
    if len(pos_fod[0]) > 0:
        view.add_component(TextStructure(create_pdb_str([elec_symbols[0]] * len(pos_fod[0]),
                           pos_fod[0])))
        view[3].clear()
        view[3].add_ball_and_stick(f'_{elec_symbols[0]}', color='red', radius=0.1)
    # Spin down FODs
    if len(pos_fod[1]) > 0:
        view.add_component(TextStructure(create_pdb_str([elec_symbols[1]] * len(pos_fod[1]),
                           pos_fod[1])))
        view[4].clear()
        view[4].add_ball_and_stick(f'_{elec_symbols[1]}', color='green', radius=0.1)
    return view


def _xyz_view(view, filename, elec_symbols):
    """Modify the view for a given XYZ file.

    Args:
        view (NGLWidget): Viewable object.
        filename (str | list | tuple): Input filename(s).
        elec_symbols (list): Identifier for up and down FODs.

    Returns:
        NGLWidget: Viewable object.
    """
    from nglview import TextStructure
    # Atoms
    atom, pos = read_xyz(filename)
    atom, pos, pos_fod = split_fods(atom, pos, elec_symbols)
    view.add_component(TextStructure(create_pdb_str(atom, pos)))
    view[0].clear()
    view[0].add_ball_and_stick()
    # Spin up FODs
    if len(pos_fod[0]) > 0:
        view.add_component(TextStructure(create_pdb_str([elec_symbols[0]] * len(pos_fod[0]),
                           pos_fod[0])))
        view[1].clear()
        view[1].add_ball_and_stick(f'_{elec_symbols[0]}', color='red', radius=0.1)
    # Spin down FODs
    if len(pos_fod[1]) > 0:
        view.add_component(TextStructure(create_pdb_str([elec_symbols[1]] * len(pos_fod[1]),
                           pos_fod[1])))
        view[2].clear()
        view[2].add_ball_and_stick(f'_{elec_symbols[1]}', color='green', radius=0.1)
    view.center()
    return view


def _traj_view(view, filename):
    """Modify the view for a given TRAJ file.

    Args:
        view (NGLWidget): Viewable object.
        filename (str | list | tuple): Input filename(s).

    Returns:
        NGLWidget: Viewable object.
    """
    try:
        from nglview.base_adaptor import Structure, Trajectory
    except ImportError:
        log.exception('Necessary dependencies not found. To use this module, '
                      'install them with "pip install eminus[viewer]".\n\n')
        raise

    class eminusTrajectory(Trajectory, Structure):
        """eminusTrajectory object to handle trajectory files.

        The interface replicates the Trajectory classes in
        https://nglviewer.org/nglview/latest/_modules/nglview/adaptor.html

        Args:
            filenames (str | list | tuple): XYZ input file paths/names.
        """
        def __init__(self, filenames):
            """Initialize the eminusTrajectory object."""
            self.atoms = []
            if isinstance(filenames, str) and filenames.endswith(('.trj', '.traj')):
                trajectory = read_traj(filenames)
                for frame in trajectory:
                    self.atoms.append(Atoms(*frame))
            else:
                if isinstance(filenames, str) and filenames.endswith('.xyz'):
                    filenames = [filenames]
                for f in filenames:
                    self.atoms.append(Atoms(*read_xyz(f)))
            self.ext = 'pdb'
            self.params = {}
            self.id = str(uuid.uuid4())

        def get_coordinates(self, index):
            """Get the atom coordinates for a given frame.

            Args:
                index (int): Frame number.

            Returns:
                ndarray: Atom positions in Bohr.
            """
            return self.atoms[index].pos

        @property
        def n_frames(self):
            """Number of frames."""
            return len(self.atoms)

        def get_structure_string(self, index=0):
            """Get the structure string per frame in the PDB format.

            Keyword Args:
                index (int): Frame number.

            Returns:
                str: Structure string.
            """
            return create_pdb_str(self.atoms[index].atom, self.atoms[index].pos)

    trajectory = eminusTrajectory(filename)
    view.add_trajectory(trajectory)
    view.center()
    return view
