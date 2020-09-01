"""
Functions to assist with plotting the interactive EFL map
"""


def onpick(event):
    """
    Function that reacts to a `pick_event` via matplotlib connect. This
    function will highlight the selected datapoint and produce a text box
    with the datapoint's related data. Such as stadium location, distance
    away, match dates.

    :param event:
    :return:
    """
    ax = plt.gca()
    ax.texts.clear()  # This clears the text box each time a new click is done
    for coloured_dot in ax.axes.lines: # This clears the dot highlighting
        coloured_dot.remove()

    # Capturing event info
    x = gdf.iloc[event.ind[0]]['longitude']
    y = gdf.iloc[event.ind[0]]['latitude']
    club = gdf.iloc[event.ind[0]]['Club']
    stadium = gdf.iloc[event.ind[0]]['Stadium']
    distance = gdf.iloc[event.ind[0]]['distance']
    distance = str(distance) + "km"

    # Text box
    box_text = "\n".join(
        (
            f"Club: {club}",
            f"Stadium: {stadium}",
            f"Distance Away: {distance}",
        )
    )

    ax.text(-6.5, 55, box_text, bbox={'facecolor': 'blue', 'alpha': 0.5,
                                      'pad': 5})

    # Title update
    ax.set_title(
        f'You selected {club} and their stadium: {stadium}. It is {distance} '
        'away'
    )

    # Highlight the selected datapoint
    ax.plot(x, y, 'o', color='yellow')


def plot_chart(basemap, datapoints, origin):
    """
    This plots the base map (the UK), along with the associated datapoints (
    team stadium locations), and finally the origin (user's current /
    specified location).

    :param basemap: The base geographical map. For this project it would be
        the UK.
    :param datapoints: The datapoints to plot on the map. For this project it
        would be the team stadium locations.
    :param origin: The origin, this is the user's specified location.
    :return: Matplotlib Plot
    """
    basemap.plot(figsize=(10, 10), alpha=0.8)
    ax = plt.gca()
    datapoints.plot(ax=ax, color='red', picker=5)
    origin.plot(ax=ax, color='black')

    ax.set_title("Championship Away Days")
    plt.gcf().canvas.mpl_connect('pick_event', onpick)
    plt.show()


plot_chart(uk, gdf, origin_gdf)