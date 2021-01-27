import os
import pandas as pd
import plotly.graph_objects as go

DATE_FORMAT: str = '%b, %Y'

def update_layout(fig, dates) -> None:
    fig.update_layout(
        xaxis={
            'tickvals': dates,
            'tickformat': DATE_FORMAT,
            'tickangle': 45,
            'ticks': 'outside',
            'ticklen': 5,
            'tickwidth': 2,
            'showline': True, 
            'linewidth': 2, 
            'linecolor': 'black',
            'tickfont': {'size': 14},
        },
        yaxis={
            'showgrid': True,
            'gridwidth': 0.5,
            'gridcolor': '#B0BEC5',
            'ticks': 'outside',
            'ticklen': 5,
            'tickwidth': 2,
            'showline': True, 
            'linewidth': 2, 
            'linecolor': 'black',
            'tickfont': {'size': 14},
            'tick0': 0,
            'dtick': 10,
        },
        plot_bgcolor="white",
        legend={'orientation': 'h', 'x': 0, 'y': 1.2}
    )

if __name__ == '__main__':
    data_path: str = os.path.join('data', 'metrics')
    daostack_main: pd.DataFrame = pd.read_csv(
        os.path.join(data_path, 'daostack_active_daos_mainnet.csv'), 
        header=0)
    daohaus_main: pd.DataFrame = pd.read_csv(
        os.path.join(data_path, 'daohaus_active_daos_mainnet.csv'), 
        header=0)
    aragon_main: pd.DataFrame = pd.read_csv(
        os.path.join(data_path, 'aragon_active_daos_mainnet.csv'), 
        header=0)
    daostack_xdai: pd.DataFrame = pd.read_csv(
        os.path.join(data_path, 'daostack_active_daos.csv'), 
        header=0)
    daohaus_xdai: pd.DataFrame = pd.read_csv(
        os.path.join(data_path, 'daohaus_active_daos.csv'), 
        header=0)
    aragon_xdai: pd.DataFrame = pd.read_csv(
        os.path.join(data_path, 'aragon_active_daos.csv'), 
        header=0)

    # plot result
    fig = go.Figure(
        data=[
            go.Scatter(
                x=daostack_main['createdAt'], 
                y=daostack_main['count'],
                name='DAOstack (only mainnet)',
                mode='lines+markers',
                marker_color='#A5D6A7',
                marker_symbol='circle-open',
                marker_size=7),
            go.Scatter(
                x=daostack_xdai['createdAt'], 
                y=daostack_xdai['count'],
                name='DAOstack',
                mode='lines+markers',
                marker_color='#388E3C',
                marker_symbol='circle',
                marker_size=7),
            go.Scatter(
                x=daohaus_main['createdAt'], 
                y=daohaus_main['count'],
                name='DAOhaus (only mainnet)',
                mode='lines+markers',
                marker_color='#FFCC80',
                marker_symbol='diamond-tall-open',
                marker_size=7),
            go.Scatter(
                x=daohaus_xdai['createdAt'], 
                y=daohaus_xdai['count'],
                name='DAOhaus',
                mode='lines+markers',
                marker_color='#F57C00',
                marker_symbol='diamond-tall',
                marker_size=7),
            go.Scatter(
                x=aragon_main['date'], 
                y=aragon_main['count'],
                name='Aragon (only mainnet)',
                mode='lines+markers',
                marker_color='#90CAF9',
                marker_symbol='x-open',
                marker_size=7),
            go.Scatter(
                x=aragon_xdai['date'], 
                y=aragon_xdai['count'],
                name='Aragon',
                mode='lines+markers',
                marker_color='#1976D2',
                marker_symbol='x',
                marker_size=7),
    ])
    update_layout(fig, dates=aragon_main['date'])
    fig.show()
