"""
3D Volume viewer for medical imaging
func:
    animation_viewer: display as a animation
    multi_slice_viewer: press key `left`/`right` to shift to previous/next slice
    multi_viewer_scroll: mouse scroll to control slice display
-----
parameter:
    volume: 3D or 4D numpy array with slice specified by 1st dimension
    interval (only for animation viewer): Delay between frames in milliseconds. Defaults to 100.
"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation


def animation_viewer(volume, interval=100):

    def updatefig(*args):
        volume = ax.volume
        ax.index = (ax.index + 1) % volume.shape[0]
        ax.images[0].set_array(volume[ax.index])
        ax.set_title('Slice ' + str(ax.index + 1))

        return ax.images[0],

    fig, ax = plt.subplots()
    ax.volume = volume
    ax.index = 0
    ax.imshow(volume[ax.index])
    ani = animation.FuncAnimation(fig, updatefig, interval=interval, blit=False)
    plt.axis('off')
    plt.show()
    return ani


def remove_keymap_conflicts(new_keys_set):
    for prop in plt.rcParams:
        if prop.startswith('keymap.'):
            keys = plt.rcParams[prop]
            remove_list = set(keys) & new_keys_set
            for key in remove_list:
                keys.remove(key)


def multi_slice_viewer(volume):
    remove_keymap_conflicts({'left', 'right'})
    fig, ax = plt.subplots()
    ax.volume = volume
    ax.index = volume.shape[0] // 2
    ax.imshow(volume[ax.index])
    ax.set_title('Slice ' + str(ax.index))
    fig.canvas.mpl_connect('key_press_event', process_key)


def multi_viewer_scroll(volume):
    fig, ax = plt.subplots()
    ax.volume = volume
    ax.index = volume.shape[0] // 2
    ax.imshow(volume[ax.index])
    ax.set_title('Slice ' + str(ax.index))
    fig.canvas.mpl_connect('scroll_event', scroll_mouse)



def process_key(event):
    fig = event.canvas.figure
    ax = fig.axes[0]
    if event.key == 'left':
        previous_slice(ax)
    elif event.key == 'right':
        next_slice(ax)
    fig.canvas.draw()


def scroll_mouse(event):
    fig = event.canvas.figure
    ax = fig.axes[0]
    if event.button == 'up':
        previous_slice(ax)
    elif event.button == 'down':
        next_slice(ax)
    fig.canvas.draw()


def previous_slice(ax):
    """Go to the previous slice."""
    volume = ax.volume
    ax.index = (ax.index - 1) % volume.shape[0]  # wrap around using %
    ax.images[0].set_array(volume[ax.index])
    ax.set_title('Slice ' + str(ax.index))


def next_slice(ax):
    """Go to the next slice."""
    volume = ax.volume
    ax.index = (ax.index + 1) % volume.shape[0]
    ax.images[0].set_array(volume[ax.index])
    ax.set_title('Slice ' + str(ax.index))