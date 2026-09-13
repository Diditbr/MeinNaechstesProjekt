import numpy as np
import matplotlib.pyplot as plt

class UnwuchtBerechnung:
    """
    Berechnung der dynamischen Unwucht eines Zylinders auf einer Welle
    """
    
    def __init__(self, aussendurchmesser, innendurchmesser, wellenlange, 
                 zylinderlange, versatz_axial, versatz_links, versatz_rechts,
                 drehzahl, dichte_zylinder, dichte_welle):
        """
        Parameter:
        - aussendurchmesser: Außendurchmesser des Zylinders [mm]
        - innendurchmesser: Innendurchmesser / Wellendurchmesser [mm]
        - wellenlange: Länge der Welle [mm]
        - zylinderlange: Länge des Zylinders [mm]
        - versatz_axial: Mittenversatz des Zylinders in axialer Richtung [mm]
        - versatz_links: Mittenversatz links [mm]
        - versatz_rechts: Mittenversatz rechts [mm]
        - drehzahl: Drehzahl [U/min]
        - dichte_zylinder: Dichte Zylinder [kg/dm³]
        - dichte_welle: Dichte Welle [kg/dm³]
        """
        self.d_aus = aussendurchmesser / 10  # Umrechnung auf cm
        self.d_in = innendurchmesser / 10
        self.l_welle = wellenlange / 10
        self.l_zyl = zylinderlange / 10
        self.versatz_axial = versatz_axial / 10
        self.versatz_links = versatz_links / 10
        self.versatz_rechts = versatz_rechts / 10
        self.n = drehzahl
        self.rho_zyl = dichte_zylinder
        self.rho_welle = dichte_welle
        
    def berechne_masse_zylinder(self):
        """Berechnung der Zylindermasse"""
        r_aus = self.d_aus / 2
        r_in = self.d_in / 2
        volumen = np.pi * (r_aus**2 - r_in**2) * self.l_zyl
        # Volumen liegt in cm³ vor, die Dichte in kg/dm³.
        masse = volumen * self.rho_zyl / 1000
        return masse
    
    def berechne_masse_welle(self):
        """Berechnung der Wellenmasse"""
        r_in = self.d_in / 2
        volumen = np.pi * r_in**2 * self.l_welle
        # Volumen liegt in cm³ vor, die Dichte in kg/dm³.
        masse = volumen * self.rho_welle / 1000
        return masse
    
    def berechne_schwerpunkt_zylinder(self):
        """Berechnung des Schwerpunkts des Zylinders"""
        r_aus = self.d_aus / 2
        # Radiale Exzentrizität (zur Wellenmittellinie)
        r_s = (r_aus - self.d_in / 2) / 2 + self.d_in / 2
        return r_s
    
    def berechne_unwucht_momente(self):
        """Berechnung der Unwuchtmomente an linker und rechter Seite"""
        m_zyl = self.berechne_masse_zylinder()
        r_s = self.berechne_schwerpunkt_zylinder()
        
        # Position des Zylinderschwerpunkts in axialer Richtung
        z_schwerpunkt = self.versatz_axial
        
        # Unwucht an linker Seite (mit Versatz links)
        U_links = m_zyl * r_s * self.versatz_links
        
        # Unwucht an rechter Seite (mit Versatz rechts)
        U_rechts = m_zyl * r_s * self.versatz_rechts
        
        return U_links, U_rechts
    
    def berechne_unwucht_gesamtsystem(self):
        """Berechnung der Unwucht des Gesamtsystems"""
        U_links, U_rechts = self.berechne_unwucht_momente()
        
        # Gesamtunwucht (Vektorsumme)
        U_gesamt = np.sqrt(U_links**2 + U_rechts**2)
        
        return U_gesamt, U_links, U_rechts
    
    def berechne_resonanzfrequenz(self):
        """Berechnung der Resonanzfrequenz (vereinfacht)"""
        # Omega in rad/s
        omega = self.n * 2 * np.pi / 60
        return omega
    
    def berechne_amplituden(self):
        """Berechnung der Auslenkungsamplituden"""
        U_gesamt, U_links, U_rechts = self.berechne_unwucht_gesamtsystem()
        omega = self.berechne_resonanzfrequenz()
        m_gesamt = self.berechne_masse_zylinder() + self.berechne_masse_welle()
        
        # Amplitude = Unwucht / (Masse * omega²)
        if m_gesamt > 0:
            A = U_gesamt / (m_gesamt * omega**2)
        else:
            A = 0
        
        return A, U_gesamt
    
    def ausgabe_ergebnisse(self):
        """Ausgabe der berechneten Ergebnisse"""
        print("=" * 60)
        print("UNWUCHTBERECHNUNG EINES ZYLINDERS AUF EINER WELLE")
        print("=" * 60)
        
        print("\nEINGABEPARAMETER:")
        print(f"Außendurchmesser Zylinder: {self.d_aus * 10:.2f} mm")
        print(f"Innendurchmesser / Wellendurchmesser: {self.d_in * 10:.2f} mm")
        print(f"Wellenlänge: {self.l_welle * 10:.2f} mm")
        print(f"Zylinderlänge: {self.l_zyl * 10:.2f} mm")
        print(f"Mittenversatz (axial): {self.versatz_axial * 10:.2f} mm")
        print(f"Mittenversatz Links: {self.versatz_links * 10:.2f} mm")
        print(f"Mittenversatz Rechts: {self.versatz_rechts * 10:.2f} mm")
        print(f"Drehzahl: {self.n:.2f} U/min")
        print(f"Dichte Zylinder: {self.rho_zyl:.2f} kg/dm³")
        print(f"Dichte Welle: {self.rho_welle:.2f} kg/dm³")
        
        print("\nBERECHNETE WERTE:")
        m_zyl = self.berechne_masse_zylinder()
        m_welle = self.berechne_masse_welle()
        print(f"Masse Zylinder: {m_zyl:.4f} kg")
        print(f"Masse Welle: {m_welle:.4f} kg")
        print(f"Gesamtmasse: {m_zyl + m_welle:.4f} kg")
        
        U_gesamt, U_links, U_rechts = self.berechne_unwucht_gesamtsystem()
        print(f"\nUnwucht links: {U_links:.4f} kg·cm")
        print(f"Unwucht rechts: {U_rechts:.4f} kg·cm")
        print(f"Gesamtunwucht: {U_gesamt:.4f} kg·cm")
        print(f"Unwucht links: {U_links * 1e7:.4f} mg·mm")
        print(f"Unwucht rechts: {U_rechts * 1e7:.4f} mg·mm")
        print(f"Gesamtunwucht: {U_gesamt * 1e7:.4f} mg·mm")
        
        A, _ = self.berechne_amplituden()
        print(f"\nAuslenkungsamplitude: {A * 10:.6f} mm")
        
        omega = self.berechne_resonanzfrequenz()
        print(f"Winkelgeschwindigkeit: {omega:.2f} rad/s")
        
        print("=" * 60)


# Beispielberechnung
if __name__ == "__main__":
    # Eingabeparameter
    aussendurchmesser = 20  # mm
    innendurchmesser = 6    # mm (Wellendurchmesser)
    wellenlange = 80        # mm
    zylinderlange = 40       # mm
    versatz_axial = 10        # mm (Mittenversatz axial)
    versatz_links = 0.01        # mm
    versatz_rechts = 0     # mm
    drehzahl = 1500          # U/min
    dichte_zylinder = 4.6   # kg/dm³ (Stahl)
    dichte_welle = 7.85      # kg/dm³ (Stahl)
    
    # Berechnung durchführen
    unwucht = UnwuchtBerechnung(aussendurchmesser, innendurchmesser, wellenlange,
                               zylinderlange, versatz_axial, versatz_links, 
                               versatz_rechts, drehzahl, dichte_zylinder, dichte_welle)
    
    unwucht.ausgabe_ergebnisse()
