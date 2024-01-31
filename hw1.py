import json
import pandas as pd
import plotly.graph_objects as go


def _code_mapping(df, src, targ):
    """ Map labels in src and targ to integers """

    # get distinct labels
    labels = sorted(set(list(df[src]) + list(df[targ])))

    # get integer codes
    codes = list(range(len(labels)))

    # create label to code mapping
    lc_map = dict(zip(labels, codes))

    # substitute names for codes in the dataframe
    df = df.replace({src: lc_map, targ: lc_map})

    return df, labels


def make_sankey(df, src, targ, vals=None, **kwargs):
    """
   :param df: Input dataframe
   :param src: Source column of labels
   :param targ: Target colum of labels
   :param vals: Thickness of the link for each row
   :return:
   """
    if vals:
        values = df[vals]
    else:
        values = [1] * len(df)  # all 1's

    df, labels = _code_mapping(df, src, targ)
    line_color = kwargs.get('line_color', 'black')
    width = kwargs.get('width', 2)
    link = {'source': df[src], 'target': df[targ], 'value': values,
            'line': {'color': line_color, 'width': width}}

    node = {'label': labels}

    sk = go.Sankey(link=link, node=node)
    fig = go.Figure(sk)
    fig.show()


def main():
    # step 1
    f = open("/Users/daimon/DS3500/artists.json")
    artists = json.load(f)
    # "Nationality"3, "Gender"4, "BeginDate"5

    f.close()
    artists_df = pd.DataFrame.from_dict(artists)
    artists_info_df = artists_df.loc[:, "Nationality":"BeginDate"]
    artists_info_df["Decade"] = artists_info_df["BeginDate"].apply(lambda x: int(x) - (int(x) % 10))
    artists_info_df.drop(["BeginDate"], axis=1, inplace=True)
    # print(artists_info_df)

    # step 3 & 4
    artists_filtered = artists_info_df.query("Decade != 0 and Decade.notna() and Nationality.notna()"
                                                   "and Gender.notna()")
    artists_filtered.loc[:, "Decade"] = artists_filtered.loc[:, "Decade"].apply(str)
    #print(artists_filtered)

    # steps 2
    artists1 = artists_filtered.groupby(['Nationality', 'Decade'])["Gender"].count().reset_index(name="count")
    artists1 = artists1.query("count > 20")
    # print(artists_filtered)

    print(artists1)
    # step 5
    make_sankey(artists1, 'Nationality', 'Decade', line_color='green', vals='count', width=0)

    # step 6
    artists2 = artists_filtered.groupby(['Nationality', 'Gender'])['Decade'].count().reset_index(name="count")
    artists2 = artists2.query('count > 20')

    make_sankey(artists2, 'Nationality', 'Gender', line_color='green', vals='count', width=0)

    # step 7
    artists3 = artists_filtered.groupby(['Gender', 'Decade'])['Nationality'].count().reset_index(name="count")
    artists3 = artists3.query('count > 20')

    make_sankey(artists3, 'Gender', 'Decade', line_color='green', vals='count', width=0)

    print(artists1, artists2, artists3)

if __name__ == "__main__":
    main()
