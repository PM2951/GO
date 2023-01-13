import streamlit as st  
import pandas as pd
from matplotlib.colors import LogNorm
from matplotlib import pyplot as plt
from io import BytesIO
import matplotlib.font_manager as fm

FONT_PATH = '/content/virtual_libraries/src/python/fonts/Arial.ttf'
fp = fm.FontProperties(fname=FONT_PATH) 

font_files = fm.findSystemFonts(fontpaths='/content/virtual_libraries/src/python/fonts/')
for font_file in font_files:
    fm.fontManager.addfont(font_file)
plt.rcParams['font.family'] = 'Arial'

st.title('GO heatmap maker')

txt = st.text_area('GOデータをエクセルからコピペ↓')

if len(txt) !=0:
    txt=txt.splitlines()
    txt=[s.split("\t") for s in txt ]
    data = pd.DataFrame(txt)
    h = data.iloc[0]
    data.columns = h
    data=data.drop(data.index[0])
    data=data.reset_index(drop=True)
    
    fig=plt.figure(figsize=[8,6])
    plt.rcParams['figure.subplot.bottom'] = 0.2
    
    header_data = list(data)
        
    st.subheader("select GO, FoldEnrichment, P-value, and Gnen count")
    options = st.multiselect('Select four datas!', header_data)
        
    if len(options) !=4 :
        st.dataframe(data)
    else:
        tab1, tab2 = st.tabs(["📈 Graph", "🗃 Data"])
        tab1.subheader("A tab with a graph")
        with tab1.container():
        #sidebar
            height = st.sidebar.number_input('Figure size (height)', value =6)
            width = st.sidebar.number_input('Figure size (width)', value =8)
            ordering = st.sidebar.selectbox('順序（何順にソートするか）', ('FoldEnrichment','P-value'))
            count = st.sidebar.number_input('GOの数', value=10)
            vmax = st.sidebar.number_input('MAX p-value (書き方 「1e-1」)', value =1e-1)
            vmin = st.sidebar.number_input('min p-value (書き方 「1e-20」)', value =1e-20)
            color = st.sidebar.selectbox('Color', ('Greys_r','spring','summer','autumn','Spectral','brg','gnuplot','gist_heat', 'hot','Blues_r', 'viridis', 'plasma', 'cividis', 'PuRd_r', 'RdPu_r', 'BuPu_r'))
            times = st.sidebar.number_input('Plot size', value =1.5)
            n = st.sidebar.number_input('GeneCountの数', value =3)
        #main
            fig.set_figheight(height)
            fig.set_figwidth(width)
            fe_float= pd.Series(data[options[1]], dtype=float)
            p_float = pd.Series(data[options[2]], dtype=float)
            data['FoldEnrichment(float)'] = fe_float
            data['pvalue(float)'] = p_float
            if ordering == 'FoldEnrichment':
              df = data.sort_values('FoldEnrichment(float)', ascending=False)
              df_n = df[:count]
              df_n = df_n.sort_values('FoldEnrichment(float)')
            elif ordering == 'P-value':
              df = data.sort_values('pvalue(float)', ascending=True)
              df_n = df[:count]
              df_n = df_n.sort_values('pvalue(float)',ascending=False)
            d1 = pd.Series(df_n[options[0]])
            d2 = pd.Series(df_n[options[1]], dtype=float)
            d3 = pd.Series(df_n[options[2]], dtype=float)
          #sidebar
            xmin = st.sidebar.number_input('x軸の最小値', value=d2.min())
            xmax = st.sidebar.number_input('x軸の最大値', value=d2.max())
            xlabel = st.sidebar.text_input('x軸ラベル',options[1])
            xlabelsize = st.sidebar.number_input('x軸ラベルサイズ', value = 12.0)
            xsize = st.sidebar.number_input('x軸フォントサイズ', value =12.0)
            ysize = st.sidebar.number_input('y軸フォントサイズ', value =12.0)
          #main
            plt.xlabel(xlabel, fontsize = xlabelsize)
            plt.xticks(fontsize=xsize)
            plt.yticks(fontsize=ysize)
            cm = plt.cm.get_cmap(color)
            size =  pd.Series(df_n[options[3]], dtype=float)
            size = times*size
            plt.scatter(d2, d1, c=d3, s=size, 
                        linewidths=0.5,
                        edgecolors = 'black', 
                        norm=LogNorm(vmax=vmax, vmin=vmin), 
                        cmap=cm, 
                        zorder=2,
                        )
            plt.colorbar()
            plt.xlim(xmin, xmax)
            cmax = size.max()
            for i in (range(0,n)):
                i = i+1
                size_i = cmax *i/n
                l = (cmax/times) *i/n
                label =  round(l)
                plt.scatter([],[],c='k',s=size_i, label=label)
            plt.legend(loc="upper right",bbox_to_anchor=(.5, -.15), frameon=False,ncol=6, prop=fp)
            plt.subplots_adjust(left=0.6, right=0.95)
            st.pyplot(fig)
            col1, col2= st.columns([1,3])
            with col1:
                fig_exten = st.selectbox('拡張子を選択',('pdf','png', 'jpg','svg'))
            with col2:
                dpi = st.slider('解像度（dpi）', 300, 900, 300)
            trspt = st.checkbox('背景を透明にする')
            ofs = BytesIO()
            fig.savefig(ofs, format=fig_exten, dpi=int(dpi), transparent=trspt)
            png_data = ofs.getvalue()
            st.caption('Click to download')
            st.download_button(
                label=f"{fig_exten}のダウンロード",
                data=png_data,
                file_name="fig."+str(fig_exten),
                mime="application/octet-stream",
            )
            
        with tab2.container():
            st.subheader("A tab with the data")
            st.dataframe(df)
            st.markdown('パラメータ')
            st.write(f'Number of GO: {count}',f'P-value(MAX): {vmax}',f'P-value(min): {vmin}', f'size: x{times}')

else:
    columns1 = ['GO biological process complete',
            'Arabidopsis thaliana - REFLIST (27430)', 'upload_1 (2432)', 'upload_1 (expected)', 'upload_1 (over/under)', 'upload_1 (fold Enrichment)', 'upload_1 (P-value)']
    list1=[['cellular response to decreased oxygen levels (GO:0036294)',240,120,21.28,'+',5.64,'1E-10'],
            ['cellular response to hypoxia (GO:0071456)',238,119,21.10,'+',5.64,'5.16E-39']]
    df1 = pd.DataFrame(data=list1, columns=columns1)
    st.write('・Pantherから取得したGOのデータを使う。')
    st.write('（参考のデータ↓）')
    st.table(df1)
