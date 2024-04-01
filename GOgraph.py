import requests
import streamlit as st
import pandas as pd
from matplotlib.colors import LogNorm
from matplotlib import pyplot as plt
from io import BytesIO
import matplotlib.font_manager as fm

FONT_PATH = '/content/GO/font/Arial.ttf'
fp = fm.FontProperties(fname=FONT_PATH)

font_files = fm.findSystemFonts(fontpaths='/content/GO/font/')
for font_file in font_files:
    fm.fontManager.addfont(font_file)
plt.rcParams['font.family'] = 'Arial'

# def term_cov(x):
#     if 'id' in x:
#       id = x['id']
#       label = x['label']
#       name = f'{label}({id})'
#     else:
#       name = x['label']
#     return name

# def pantherGO(gene_list):
#     base_url = "https://pantherdb.org/"
#     endpoint = "services/oai/pantherdb/enrich/overrep"
#     params = {
#         "geneInputList": ','.join(gene_list),  # 遺伝子リスト
#         "organism": "3702",
#         "annotDataSet": 'GO:0008150',
#         "enrichmentTestType": "FISHER",
#         "correction": "BONFERRONI",
#     }
#     response = requests.post(base_url + endpoint, params=params)
#     result_df = pd.DataFrame(response.json()['results']['result'])
#     if len(result_df) == 0:
#         raise ValueError('遺伝子リストが空です！')
#     try:
#       result_df_sig = result_df[(result_df['pValue'] < 0.05) & (
#           result_df['fold_enrichment'] > 0)].copy()
#       result_df_sig = result_df_sig.sort_values(
#           by='fold_enrichment', ascending=False)
#       result_df_sig['term'] = result_df_sig['term'].apply(term_cov).copy()
#       # reference = response.json()['results']['reference']
#       # input_list = response.json()['results']['input_list']
#       result_df_sig = result_df_sig[[
#           'term', 'number_in_list', 'fold_enrichment', 'pValue']]
#     # print(result_df_sig)
#       return result_df_sig
#     except:
#         raise ValueError('エラー')


def make_graph(data, height, width, count, vmax, vmin, cmap, plotsize, xmin, xmax, n=3):
    fig = plt.figure(figsize=(width, height))
    data['fold_enrichment'] = data['fold_enrichment'].astype(float)
    module_GO_top = data.sort_values(by='fold_enrichment', ascending=False).head(int(count))
    module_GO_top = module_GO_top.sort_values(
        by='fold_enrichment', ascending=True)
    y = module_GO_top['term']
    x = module_GO_top['fold_enrichment'].astype(float)
    c = module_GO_top['pValue'].astype(float)
    size = module_GO_top['number_in_list'].astype(int)
    
    plt.scatter(x, y, c=c, s=size*plotsize, linewidths=0.5,
                edgecolors='black', cmap=cmap,
                norm=LogNorm(vmax=vmax, vmin=vmin))

    # グラフの設定
    plt.xlabel('fold enrichment')
    plt.ylabel('GO term')
    plt.xlim(xmin, xmax)
    colorbar = plt.colorbar()
    colorbar.set_label(label='P-value', rotation=-90, labelpad=15)
    # gene count
    for i in (range(0, n)):
        i = i+1
        size_i = size.max()*plotsize * i/n
        l = (size.max()) * i/n
        label = round(l)
        plt.scatter([], [], c='k', s=size_i, label=label)
    plt.legend(loc="upper right", bbox_to_anchor=(0.5, -0.15),
               frameon=False, ncol=6, title='Gene count', prop=fp)
    plt.tight_layout()
    st.pyplot(fig)
    return fig


st.title('GO heatmap Graph')
st.sidebar.write('')

txt = st.text_area('Panther GOの結果をペースト')

#sidebars
height = st.sidebar.number_input('Figure size (height)', value=12)
width = st.sidebar.number_input('Figure size (width)', value=6)
count = st.sidebar.number_input('GOの数', value=10)
vmax = st.sidebar.number_input('MAX p-value (書き方 「1e-1」)', value=1e-1)
vmin = st.sidebar.number_input('min p-value (書き方 「1e-20」)', value=1e-20)
cmap = st.sidebar.selectbox('Color',
                            ('Greys_r', 'spring', 'summer', 'autumn', 'Spectral', 'brg', 'gnuplot', 'YlGnBu',
                                'gist_heat', 'hot', 'Blues_r', 'viridis', 'plasma', 'cividis', 'PuRd_r', 'RdPu_r', 'BuPu_r',
                                ))
plotsize = st.sidebar.number_input('Plot size', value=1.5)
n = st.sidebar.number_input('GeneCountの数', value=3)
xmin = st.sidebar.number_input('x軸の最小値', value=0)
xmax = st.sidebar.number_input('x軸の最大値', value=50)
fontsize = st.sidebar.number_input('フォントサイズ', value=12)
caption = st.sidebar.write('='*20)

plt.rcParams.update({'font.size': fontsize})
if len(txt) != 0:
    txt = txt.splitlines()
    txt = [s.split("\t") for s in txt]
    data = pd.DataFrame(txt)
    h = data.iloc[0]
    data.columns = h
    data = data.drop(data.index[0])
    data = data.reset_index(drop=True)
    data.columns = ['term', 'REFLIST (27430)', "number_in_list",
                    "expected count", "(over/under)", "fold_enrichment", "pValue"]
    st.write(data)
    if len(data) > 0:
        # GOグラフ作成
        data = data
        fig = make_graph(data, height, width, count, vmax,
                         vmin, cmap, plotsize, xmin, xmax)
        # st.pyplot(fig)
        col1, _ = st.columns([2, 2])
        with col1:
            fig_exten = st.selectbox('拡張子を選択', ('pdf', 'png', 'jpg', 'svg'))
        col2, _ = st.columns([2, 2])
        with col2:
            padding = st.number_input('余白サイズ', value=20)
        col3, _ = st.columns([2, 2])
        with col3:
            dpi = st.slider('解像度（dpi）', 300, 900, 300)
        trspt = st.checkbox('背景を透明にする')
        ofs = BytesIO()
        fig.savefig(ofs, format=fig_exten, dpi=int(dpi),
                    transparent=trspt, pad_inches=padding)
        png_data = ofs.getvalue()
        st.caption('Click to download')
        st.download_button(
            label=f"{fig_exten}のダウンロード",
            data=png_data,
            file_name="fig."+str(fig_exten),
            mime="application/octet-stream",
        )

