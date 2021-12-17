import streamlit as st
import plotly.express as px
import pandas as pd
import json

# Membaca isi file
def load_data_excel():
    data=pd.read_csv("produksi_minyak_mentah.csv")
    data=data[data["produksi"]>=0]
    data=data[data["tahun"]>0]
    return data

def run_status():
    latest_iteration = st.empty()
    bar = st.progress(0)
    for i in range (100):
        latest_iteration.text(f"Percent Complate {i+1}")
        bar.progress (i+1)
        time.sleep(0.1)
        st.empty()
# Fungsi untuk mencari negara
def kode_negara(kode, jsn) :

    for i in jsn :

        if kode == i[1] :
            kname = str(i[0])
            kode_neg = ("Kode Negara : " + i[2])
            reg = ("Region : " + i[3])
            sub_reg = ("Subregion : " + i[4])
            break

        else :
            kname = ""
            kode_neg = ""
            reg = ""
            sub_reg = ""

    return kname, kode_neg, reg, sub_reg

#Membaca file excel dan json
data=load_data_excel()
with open('kode_negara_lengkap.json') as f:
    jh = json.load(f)
    #membuat dict
    dict = []
    for i in jh:
        nama = i.get('name')
        code = i.get('alpha-3')
        country_code = i.get('country-code')
        region = i.get('region')
        subregion = i.get('sub-region')
        dict.append([nama, code, country_code, region, subregion])

#Konfigurasi
st.set_page_config(page_title="uas_12220040",
                    page_icon=":bar_chart:",
                    layout="wide")
st.markdown(
        "###### Made in [![this is an image link](https://i.imgur.com/iIOA6kU.png)](https://www.streamlit.io/)&nbsp, with :smile: by [@Dharmatsaniya](https://www.instagram.com/dharmatsaniya/) &nbsp | &nbsp [![Follow](https://img.shields.io/twitter/follow/dharmatsaniya?style=social)](https://twitter.com/dharmatsaniya) &nbsp "
    )

# Membuat simbol icon
st.title(":droplet: Produksi Minyak Mentah di Dunia")
st.markdown("##")

#Menu
option_menu=st.sidebar.selectbox(
    'Menu',('Home','Soal A','Soal B','Soal C','Soal D','About Me')
)
#condition home
if option_menu == 'Home'or option_menu ==' ':
    colomhome,colom1=st.columns(2)
    st.sidebar.image("home.jpg", use_column_width=True)
    with colomhome:
        st.subheader('HOME')
        st.image("peta.jpg", width=500,caption='Peta Dunia <www.bola.com>')
    with colom1:
        st.write("Data Produksi Minyak Mentah Dunia")
        data=load_data_excel()
        data
        st.subheader("Scatter Sebaran Produksi Per tahun")
    fig = px.scatter(data, x="tahun", y="produksi",
                size="produksi",color="kode_negara",hover_name="tahun",
                log_x=True, size_max=55, range_x=[1971,2015],range_y=[1971,4000000],
                animation_frame="tahun",animation_group="kode_negara")
    fig.update_layout(width=800)
    st.write(fig)
    

#SOAL BAGIAN A
#condition A
elif option_menu == 'Soal A':
    #input user
    st.subheader("Grafik Jumlah Produksi Minyak Mentah Terhadap Waktu (tahun) dari Suatu Negara N")
    opsi_negara = st.selectbox("Pilih Negara : ", options=(i[0] for i in dict))
    
    for i in dict:
        if i[0] == opsi_negara :
            country_code = i[1]
    #condtional
    if not((data['kode_negara'] == country_code).any()) :
        
        st.error("Tidak Ditemukan Data Produksi Minyak Mentah Negara " + opsi_negara)
    
    else :

        with st.expander('Klik untuk melihat Grafik negara '+ opsi_negara ):
            display_data = data[data["kode_negara"] == country_code][['tahun', 'produksi']]
            display_data = display_data.rename(columns={'tahun':'Tahun'}).set_index('Tahun')
            st.line_chart(display_data)
    

# SOAL BAGIAN B
#condtional B
elif option_menu == 'Soal B':

    st.subheader('Grafik B-besar Negara dengan Jumlah Produksi Terbesar per Tahun')

    opsi_tahun = st.sidebar.slider('Pilih Tahun : ',1971,max(data["tahun"]),step=1 )
    data_frame = data.query('tahun == @opsi_tahun')

    besar = (st.sidebar.slider('Pilih Jumlah Negara Terbesar : ', 1, data_frame['kode_negara'].nunique(),step=1 ))
    besar_data = data_frame.nlargest(int(besar), 'produksi')

    judul_b = "Grafik {jumlah} Besar Negara dengan Jumlah Produksi Terbesar pada Tahun {tahunnya}".format(jumlah = besar, tahunnya = opsi_tahun)
    with st.expander('Klik untuk melihat Grafik  negara dengan jumlah produksi terbesar pada tahun '+ str(opsi_tahun)):
        chartb = data.loc[data["tahun"] == int(opsi_tahun)].sort_values(["produksi"], ascending=[0])
        chartb = chartb[:int(besar)].reset_index(drop=True)
        chartb_ = chartb[['kode_negara', 'produksi']].rename(columns={'kode_negara':'negara'}).set_index('negara')
        st.bar_chart(chartb_)
        st.write(chartb)
        
        

# SOAL BAGIAN C
#condtional C
elif option_menu=='Soal C':
    #tulisan tampilan
    st.subheader('Grafik B-Besar Negara dengan Jumlah Produksi Terbesar Secara Kumulatif Seluruh Tahun')
    st.write('Soal Bagian C')
    
    #Tabel Akumulatif
    data_kum = data['kode_negara'].ne(data['kode_negara'].shift()).cumsum()
    data['kumulatif'] = data.groupby(data_kum)['produksi'].cumsum()
    
    kumulatif = data[['kode_negara', 'produksi', 'kumulatif']]
    kumulatif = kumulatif.sort_values('kumulatif', ascending=False).drop_duplicates(subset=['kode_negara'])

    option_jumlah = int(st.slider('Pilih Jumlah Negara Terbesar : ', 1, kumulatif['kode_negara'].nunique()))
    data_kumulatif = kumulatif.nlargest(option_jumlah, 'kumulatif')
    #membuat grafik
    with st.expander("Klik untuk melihat grafik produksi terbesar secara kumulatif tahun"):
        chartc = (data[['kode_negara', 'produksi']].groupby('kode_negara', as_index=False).sum().sort_values(['produksi'], ascending=[0])).reset_index(drop=True)
        chartc = chartc[:int(option_jumlah)].reset_index(drop=True)
        chart_ = chartc[['kode_negara', 'produksi']].rename(columns={'kode_negara':'negara'}).set_index('negara')
        st.bar_chart(chart_)
        st.write(chart_)

#SOAL BAGIAN D
elif option_menu=='Soal D':
    #membaca file dan df
    df1 = pd.read_json("kode_negara_lengkap.json")
    df2 = load_data_excel() 
    df = pd.merge(df2,df1,left_on='kode_negara',right_on='alpha-3')

    #memilih tahun untuk produksi per tahun
    tahun=st.selectbox("Pilih tahun", range(1971,2016))
    
    #list negara
    lst_negara = df["name"].unique().tolist()
    lst_negara.sort()
    
    #membagi menjadi dua kolom
    colom1,colom2=st.columns(2)

    kum = df.groupby(['name', 'kode_negara', 'region', 'sub-region'])['produksi'].sum().reset_index().sort_values(by=['produksi'], ascending=False).reset_index(drop=True)
    kum_max = kum[(kum["produksi"] > 0)].iloc[0]
    kum_min = kum[(kum["produksi"] > 0)].iloc[-1]
    kum_nol = kum[(kum["produksi"] == 0)].sort_values(by=['name']).reset_index(drop=True)
    kum_nol.index += 1

    prodyear = df[(df["tahun"] == tahun)][['name', 'kode_negara', 'region', 'sub-region', 'produksi']].sort_values(by=['produksi'], ascending=False).reset_index(drop=True)
    prodyear_max = prodyear[(prodyear["produksi"] > 0)].iloc[0]
    prodyear_min = prodyear[(prodyear["produksi"] > 0)].iloc[-1]
    prodyear_nol = prodyear[(prodyear["produksi"] == 0)].sort_values(by=['name']).reset_index(drop=True)
    prodyear_nol.index += 1

    with colom1:
        st.markdown(
            f'''
            #### Negara dengan jumlah produksi terbesar pada tahun {tahun}  
            Negara: {prodyear_max["name"]}\n
            Kode negara: {prodyear_max["kode_negara"]}\n
            Region: {prodyear_max["region"]}\n
            Sub-region: {prodyear_max["sub-region"]}\n
            Jumlah produksi: {prodyear_max["produksi"]}\n
            
            #### Negara dengan jumlah produksi terkecil pada tahun {tahun}  
            Negara: {prodyear_min["name"]}\n
            Kode negara: {prodyear_min["kode_negara"]}\n
            Region: {prodyear_min["region"]}\n
            Sub-region: {prodyear_min["sub-region"]}\n
            Jumlah produksi: {prodyear_min["produksi"]}\n
            '''
        )
    with colom2:     
        st.markdown(
            f"""
            #### Negara dengan total produksi keseluruhan tahun terbesar
            Negara: {kum_max["name"]}\n
            Kode negara: {kum_max["kode_negara"]}\n
            Region: {kum_max["region"]}\n
            Sub-region: {kum_max["sub-region"]}\n
            Jumlah produksi: {kum_max["produksi"]}\n

            #### Negara dengan total produksi keseluruhan tahun terkecil
            Negara: {kum_min["name"]}\n
            Kode negara: {kum_min["kode_negara"]}\n
            Region: {kum_min["region"]}\n
            Sub-region: {kum_min["sub-region"]}\n
            Jumlah produksi: {kum_min["produksi"]}\n

        
        """)
    st.markdown(
        """
        #### Negara dengan total produksi keseluruhan tahun sama dengan nol
        
    """
    )
    kum_nol = kum_nol.drop(['produksi'], axis=1).rename(columns={"name":"Negara", "kode_negara":"Kode Negara", "region":"Region", "sub-region":"Sub Region"})
    st.dataframe(kum_nol)
    st.markdown(
        f"""
        #### Negara dengan jumlah produksi sama dengan nol pada tahun {tahun}
        
    """
    )
    prodyear_nol = prodyear_nol.drop(['produksi'], axis=1).rename(columns={"name":"Negara", "kode_negara":"Kode Negara", "region":"Region", "sub-region":"Sub Region"})
    st.dataframe(prodyear_nol)

st.sidebar.image("images.jpg", use_column_width=True)

#about me
if option_menu == 'About Me':
    st.subheader('Hello')
    colom0,colom=st.columns(2)
    with colom0:
        st.image("foto.jpg",width=200)
    with colom:
        st.subheader("Informasi Pembuat")
        st.write("Nama : Mochamad Dharma Tsaniya Rachmat")
        st.write("NIM  : 12220040")
        st.write("Kelas: Kelas-02")
        st.write("Fakultas: Teknik Perminyakan")

