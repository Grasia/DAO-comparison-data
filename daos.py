import os
import pandas as pd
import plotly.graph_objects as go
from pandas.tseries.offsets import DateOffset
from datetime import date

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
            #'tickangle': 45,
            'showline': True, 
            'linewidth': 2, 
            'linecolor': 'black',
            'tickfont': {'size': 12},
            'tick0': 0,
            'dtick': 100,
        },
        plot_bgcolor="white",
        legend={'orientation': 'h', 'x': 0, 'y': 1.2}
    )


def get_new_daos(df: pd.DataFrame, net: str, date_key: str) -> pd.DataFrame:
    dff: pd.DataFrame = df.copy()

    if net:
        dff.loc[:, :] = dff.loc[dff.network.eq(net)]
        dff.dropna(inplace=True, how='all', axis=0)

    dff.loc[:, [date_key]] = dff[[date_key]]
    #dff.loc[:, [date_key]] = dff[dff[date_key] < 1604185200]

    dff.loc[:, date_key] = pd.to_datetime(dff.loc[:, date_key], unit='s').dt.date
    dff.loc[:, date_key] = dff[date_key].apply(lambda d: d.replace(day=1))

    dff = dff.groupby([date_key]).size().reset_index(name='count')

    # generates a time series
    #today = datetime.strptime("31 October, 2020", "%d %B, %Y")
    today = date.today().replace(day=1)
    start = dff[date_key].min()
    idx = pd.date_range(start=start, end=today, freq=DateOffset(months=1))

    di_df = dict()
    rows: list = [idx, 0]
    for i, c in enumerate([date_key, 'count']):
        di_df[c] = rows[i]

    df3 = pd.DataFrame(di_df)
    df3.loc[:, date_key] = df3[date_key].dt.date

    # joinning all the data in a unique dataframe
    dff = dff.append(df3, ignore_index=True)
    dff.drop_duplicates(subset=date_key, keep="first", inplace=True)
    dff.sort_values(date_key, inplace=True)

    return dff


def get_total(news: list) -> list:
    total = [news[0]]

    for i in range(1, len(news)):
        total.append(total[i-1] + news[i])

    return total


if __name__ == '__main__':
    data_path: str = os.path.join('data', 'metrics')
    daohaus: pd.DataFrame = pd.read_csv(os.path.join(data_path, 'daohaus_daos.csv'), header=0)
    aragon: pd.DataFrame = pd.read_csv(os.path.join(data_path, 'aragon_daos.csv'), header=0)

    daohaus_main: pd.DataFrame = get_new_daos(daohaus, 'mainnet', 'timestamp')
    daohaus_xdai: pd.DataFrame = get_new_daos(daohaus, None, 'timestamp')
    aragon_main: pd.DataFrame = get_new_daos(aragon, 'mainnet', 'createdAt')
    aragon_xdai: pd.DataFrame = get_new_daos(aragon, None, 'createdAt')

    # plot result
    fig = go.Figure(
         data=[
            go.Scatter(
                x=daohaus_main['timestamp'], 
                y=get_total(daohaus_main['count'].tolist()),
                name='DAOhaus (only mainnet)',
                mode='lines+markers',
                marker_color='#FFCC80',
                marker_symbol='diamond-tall-open',
                marker_size=7),
            go.Scatter(
                x=daohaus_xdai['timestamp'], 
                y=get_total(daohaus_xdai['count'].tolist()),
                name='DAOhaus',
                mode='lines+markers',
                marker_color='#F57C00',
                marker_symbol='diamond-tall',
                marker_size=7),
            go.Scatter(
                x=aragon_main['createdAt'], 
                y=get_total(aragon_main['count'].tolist()),
                name='Aragon (only mainnet)',
                mode='lines+markers',
                marker_color='#90CAF9',
                marker_symbol='x-open',
                marker_size=7),
            go.Scatter(
                x=aragon_xdai['createdAt'], 
                y=get_total(aragon_xdai['count'].tolist()),
                name='Aragon',
                mode='lines+markers',
                marker_color='#1976D2',
                marker_symbol='x',
                marker_size=7),
    ])
    update_layout(fig, dates=aragon_main['createdAt'])
    fig.show()
