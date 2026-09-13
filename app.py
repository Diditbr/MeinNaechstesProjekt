import streamlit as st

from Unwucht import UnwuchtBerechnung


st.set_page_config(page_title="Unwuchtberechnung", page_icon="⚙️", layout="wide")

st.title("Unwuchtberechnung")
st.caption("Berechnung der dynamischen Unwucht eines Zylinders auf einer Welle")

with st.form("eingaben"):
    st.subheader("Eingabeparameter")
    left, right = st.columns(2)

    with left:
        aussendurchmesser = st.number_input("Außendurchmesser Zylinder (mm)", min_value=0.0, value=20.0)
        innendurchmesser = st.number_input("Innendurchmesser / Wellendurchmesser (mm)", min_value=0.0, value=6.0)
        wellenlange = st.number_input("Wellenlänge (mm)", min_value=0.0, value=80.0)
        zylinderlange = st.number_input("Zylinderlänge (mm)", min_value=0.0, value=40.0)
        versatz_axial = st.number_input("Mittenversatz axial (mm)", min_value=0.0, value=10.0)

    with right:
        versatz_links = st.number_input("Mittenversatz links (mm)", min_value=0.0, value=0.01, format="%.4f")
        versatz_rechts = st.number_input("Mittenversatz rechts (mm)", min_value=0.0, value=0.0)
        drehzahl = st.number_input("Drehzahl (U/min)", min_value=0.0, value=1500.0)
        dichte_zylinder = st.number_input("Dichte Zylinder (kg/dm³)", min_value=0.0, value=4.6)
        dichte_welle = st.number_input("Dichte Welle (kg/dm³)", min_value=0.0, value=7.85)

    submitted = st.form_submit_button("Berechnung durchführen", type="primary")

if submitted:
    if innendurchmesser > aussendurchmesser:
        st.error("Der Innendurchmesser darf nicht größer als der Außendurchmesser sein.")
    elif drehzahl == 0:
        st.error("Die Drehzahl muss größer als 0 U/min sein.")
    else:
        berechnung = UnwuchtBerechnung(
            aussendurchmesser,
            innendurchmesser,
            wellenlange,
            zylinderlange,
            versatz_axial,
            versatz_links,
            versatz_rechts,
            drehzahl,
            dichte_zylinder,
            dichte_welle,
        )

        masse_zylinder = berechnung.berechne_masse_zylinder()
        masse_welle = berechnung.berechne_masse_welle()
        unwucht_gesamt, unwucht_links, unwucht_rechts = berechnung.berechne_unwucht_gesamtsystem()
        amplitude, _ = berechnung.berechne_amplituden()
        winkelgeschwindigkeit = berechnung.berechne_resonanzfrequenz()

        st.subheader("Ergebnisse")
        first, second, third = st.columns(3)
        first.metric("Gesamtmasse", f"{masse_zylinder + masse_welle:.4f} kg")
        second.metric("Gesamtunwucht", f"{unwucht_gesamt * 1e7:.4f} mg·mm")
        third.metric("Auslenkungsamplitude", f"{amplitude * 10:.6f} mm")

        result_left, result_right = st.columns(2)
        with result_left:
            st.write(f"**Masse Zylinder:** {masse_zylinder:.4f} kg")
            st.write(f"**Masse Welle:** {masse_welle:.4f} kg")
            st.write(f"**Winkelgeschwindigkeit:** {winkelgeschwindigkeit:.2f} rad/s")
        with result_right:
            st.write(f"**Unwucht links:** {unwucht_links * 1e7:.4f} mg·mm")
            st.write(f"**Unwucht rechts:** {unwucht_rechts * 1e7:.4f} mg·mm")
            st.write(f"**Gesamtunwucht:** {unwucht_gesamt * 1e7:.4f} mg·mm")
