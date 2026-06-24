import streamlit as st
import numpy as np
from scipy.stats import poisson

st.set_page_config(page_title="QUANTUM STATS v6.5", layout="wide")

# CSS Stile Cyber-Neon
st.markdown("""
    <style>
    body, .main, .reportview-container { background-color: #000000 !important; color: #ffffff; }
    h1, h2, h3, h4 { font-family: 'Courier New', monospace; font-weight: bold; }
    .neon-box { padding: 15px; border-radius: 8px; margin-bottom: 12px; border: 1px solid rgba(255,255,255,0.1); background-color: #07090e; }
    .neon-1x2 { border-left: 5px solid #ff0055; box-shadow: 0 0 10px rgba(255,0,85,0.2); }
    .neon-ou { border-left: 5px solid #00d2ff; box-shadow: 0 0 10px rgba(0,210,255,0.2); }
    .neon-gg { border-left: 5px solid #00ff66; box-shadow: 0 0 10px rgba(0,255,102,0.2); }
    .neon-combo { border-left: 5px solid #cc00ff; box-shadow: 0 0 10px rgba(204,0,255,0.2); }
    .m-title { color: #8b949e; font-size: 11px; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; }
    .m-value { font-size: 22px; font-weight: bold; font-family: 'Courier New', monospace; margin-top: 2px; }
    .lbl-1x2 { color: #ff0055; } .lbl-ou { color: #00d2ff; } .lbl-gg { color: #00ff66; } .lbl-combo { color: #cc00ff; }
    .m-quota { color: #ffffff; font-size: 13px; margin-top: 4px; opacity: 0.9; font-family: monospace; }
    </style>
""", unsafe_allow_html=True)

st.title("🖥️ QUANTUM STATS v6.5 - MOTIVATIONAL xG ENGINE")
st.markdown("---")

# Database delle tue squadre per competizione
DATA_SQUADRE = {
    "Serie A": ["Atalanta", "Bologna", "Cagliari", "Como", "Fiorentina", "Frosinone", "Genoa", "Inter", "Juventus", "Lazio", "Lecce", "Milan", "Monza", "Parma", "Roma", "Sassuolo", "Torino", "Udinese", "Venezia"],
    "Premier League": ["Arsenal", "Aston Villa", "Bournemouth", "Brentford", "Brighton & Hove Albion", "Chelsea", "Coventry City", "Crystal Palace", "Everton", "Fulham", "Hull City", "Ipswich Town", "Leeds United", "Liverpool", "Manchester City", "Manchester United", "Newcastle United", "Nottingham Forest", "Sunderland", "Tottenham Hotspur"],
    "La Liga": ["Alavés", "Athletic Bilbao", "Atlético Madrid", "Barcellona", "Celta Vigo", "Deportivo La Coruña", "Elche", "Espanyol", "Getafe", "Granada", "Leganés", "Las Palmas", "Levante", "Málaga", "Osasuna", "Racing Santander", "Real Betis", "Real Madrid", "Real Sociedad", "Siviglia", "Valencia", "Villarreal"],
    "Champions League": ["Arsenal", "Manchester City", "Manchester United", "Aston Villa", "Liverpool", "Inter", "Napoli", "Roma", "Como", "FC Barcelona", "Real Madrid", "Atletico Madrid", "Villarreal FC", "Real Betis", "Bayern Monaco", "Borussia Dortmund", "RB Lipsia", "VfB Stoccarda", "Paris Saint-Germain", "RC Lens", "Lille OSC", "FC Porto", "Sporting Lisbona", "PSV Eindhoven", "Feyenoord", "Bruges", "Galatasaray", "Slavia Praga", "Shakhtar Donetsk"],
    "Europa League": ["Milan", "Juventus", "Crystal Palace", "Bournemouth", "Sunderland", "Real Sociedad", "Celta Vigo", "Hoffenheim", "Bayer Leverkusen", "Marsiglia", "Rennes", "AZ Alkmaar", "Torreense", "Beşiktaş", "R.S.C. Anderlecht", "S.L. Benfica", "HNK Hajduk Split", "FC Twente"],
    "Mondiali": ["Messico", "Sud Corea", "Repubblica Ceca", "Sudafrica", "Canada", "Svizzera", "Bosnia ed Erzegovina", "Qatar", "Brasile", "Marocco", "Scozia", "Haiti", "Stati Uniti", "Australia", "Paraguay", "Turchia", "Germania", "Costa d'Avorio", "Ecuador", "Curaçao", "Paesi Bassi", "Giappone", "Svezia", "Tunisia", "Egitto", "Iran", "Belgio", "Nuova Zelanda", "Spagna", "Uruguay", "Capo Verde", "Arabia Saudita", "Francia", "Norvegia", "Senegal", "Iraq", "Argentina", "Austria", "Algeria", "Giordania", "Colombia", "Portogallo", "Repubblica Democratica del Congo", "Uzbekistan", "Inghilterra", "Ghana", "Croazia", "Panama"]
}

# UI di selezione Competizione
competizioni = list(DATA_SQUADRE.keys())
lega_scelta = st.selectbox("Seleziona Competizione Target:", competizioni)

squadre_competizione = sorted(DATA_SQUADRE[lega_scelta])

col_in, col_out = st.columns([1, 2])

with col_in:
    st.header("🎛️ INPUT DATI REALI")
    
    idx_casa = squadre_competizione.index("Inter") if "Inter" in squadre_competizione else 0
    idx_trasf = squadre_competizione.index("Milan") if "Milan" in squadre_competizione else min(1, len(squadre_competizione) - 1)
    
    sq_casa = st.selectbox("Squadra Casa:", squadre_competizione, index=idx_casa)
    sq_trasf = st.selectbox("Squadra Trasferta:", squadre_competizione, index=idx_trasf)
    
    st.markdown("---")
    
    st.subheader(f"🏠 Parametri {sq_casa}")
    xg_fatti_h = st.number_input(f"xG Fatti Medi (Casa):", min_value=0.1, max_value=5.0, value=1.60, step=0.05)
    xg_subiti_h = st.number_input(f"xG Concessi Medi (Casa):", min_value=0.1, max_value=5.0, value=1.10, step=0.05)
    urg_h = st.slider(f"Urgenza / Aggressività {sq_casa}:", 0.50, 1.50, 1.00, step=0.05, help="1.00 è neutro. Alzalo se DEVE vincere a tutti i costi, abbassalo se gestisce.")
    
    st.markdown("---")
    
    st.subheader(f"🚀 Parametri {sq_trasf}")
    xg_fatti_a = st.number_input(f"xG Fatti Medi (Fuori):", min_value=0.1, max_value=5.0, value=1.30, step=0.05)
    xg_subiti_a = st.number_input(f"xG Concessi Medi (Fuori):", min_value=0.1, max_value=5.0, value=1.20, step=0.05)
    urg_a = st.slider(f"Urgenza / Aggressività {sq_trasf}:", 0.50, 1.50, 1.00, step=0.05, help="1.00 è neutro. Alzalo se DEVE fare il colpaccio fuori casa.")

# Calcolo delle proiezioni offensive corrette per l'urgenza tattica/motivazionale
lambda_home = xg_fatti_h * xg_subiti_a * urg_h
lambda_away = xg_fatti_a * xg_subiti_h * urg_a

# Generazione matrice delle probabilità (Poisson + Correzione Dixon-Coles)
max_g = 6
matrice = np.zeros((max_g, max_g))
for i in range(max_g):
    for j in range(max_g):
        p_h = poisson.pmf(i, lambda_home)
        p_a = poisson.pmf(j, lambda_away)
        rho = 0.10
        adj = 1.0
        if i == 0 and j == 0: adj = 1 - lambda_home * lambda_away * rho
        elif i == 1 and j == 0: adj = 1 + lambda_away * rho
        elif i == 0 and j == 1: adj = 1 + lambda_home * rho
        elif i == 1 and j == 1: adj = 1 - rho
        matrice[i, j] = p_h * p_a * adj

matrice /= np.sum(matrice)

# Calcolo mercati
p_1 = np.sum(np.tril(matrice, -1))
p_X = np.sum(np.diag(matrice))
p_2 = np.sum(np.triu(matrice, 1))
p_gg = sum(matrice[i, j] for i in range(1, max_g) for j in range(1, max_g))
p_ng = 1 - p_gg
p_o25 = np.sum(matrice[0, 3:]) + np.sum(matrice[1, 2:]) + np.sum(matrice[2, 1:]) + np.sum(matrice[3:, 0:])
p_u25 = 1 - p_o25
p_1_o25 = sum(matrice[i, j] for i in range(max_g) for j in range(max_g) if i > j and (i+j) > 2.5)
p_x_gg = sum(matrice[i, i] for i in range(1, max_g))

with col_out:
    st.header(f"📊 ANALISI MATCH: {sq_casa} vs {sq_trasf}")
    
    st.subheader("🔴 Esito Finale 1X2")
    c1, cx, c2 = st.columns(3)
    c1.markdown(f"<div class='neon-box neon-1x2'><div class='m-title'>Segno 1</div><div class='m-value lbl-1x2'>{p_1*100:.1f}%</div><div class='m-quota'>Fair: {1/p_1:.2f}</div></div>", unsafe_allow_html=True)
    cx.markdown(f"<div class='neon-box neon-1x2'><div class='m-title'>Segno X</div><div class='m-value lbl-1x2'>{p_X*100:.1f}%</div><div class='m-quota'>Fair: {1/p_X:.2f}</div></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='neon-box neon-1x2'><div class='m-title'>Segno 2</div><div class='m-value lbl-1x2'>{p_2*100:.1f}%</div><div class='m-quota'>Fair: {1/p_2:.2f}</div></div>", unsafe_allow_html=True)
    
    cm1, cm2 = st.columns(2)
    with cm1:
        st.subheader("🟢 Gol / No Goal")
        g1, g2 = st.columns(2)
        g1.markdown(f"<div class='neon-box neon-gg'><div class='m-title'>GOL</div><div class='m-value lbl-gg'>{p_gg*100:.1f}%</div><div class='m-quota'>Fair: {1/p_gg:.2f}</div></div>", unsafe_allow_html=True)
        g2.markdown(f"<div class='neon-box neon-gg'><div class='m-title'>NO GOL</div><div class='m-value lbl-gg'>{p_ng*100:.1f}%</div><div class='m-quota'>Fair: {1/p_ng:.2f}</div></div>", unsafe_allow_html=True)
    with cm2:
        st.subheader("🔵 Under / Over 2.5")
        u1, o1 = st.columns(2)
        u1.markdown(f"<div class='neon-box neon-ou'><div class='m-title'>UNDER 2.5</div><div class='m-value lbl-ou'>{p_u25*100:.1f}%</div><div class='m-quota'>Fair: {1/p_u25:.2f}</div></div>", unsafe_allow_html=True)
        o1.markdown(f"<div class='neon-box neon-ou'><div class='m-title'>OVER 2.5</div><div class='m-value lbl-ou'>{p_o25*100:.1f}%</div><div class='m-quota'>Fair: {1/(p_o25 if p_o25 > 0 else 0.01):.2f}</div></div>", unsafe_allow_html=True)

    st.subheader("🟣 Combo Professionali")
    cb1, cb2 = st.columns(2)
    cb1.markdown(f"<div class='neon-box neon-combo'><div class='m-title'>Combo 1 + Over 2.5</div><div class='m-value lbl-combo'>{p_1_o25*100:.1f}%</div><div class='m-quota'>Fair: {1/(p_1_o25 if p_1_o25 > 0 else 0.01):.2f}</div></div>", unsafe_allow_html=True)
    cb2.markdown(f"<div class='neon-box neon-combo'><div class='m-title'>Combo X + GOL</div><div class='m-value lbl-combo'>{p_x_gg*100:.1f}%</div><div class='m-quota'>Fair: {1/(p_x_gg if p_x_gg > 0 else 0.01):.2f}</div></div>", unsafe_allow_html=True)

    st.subheader("🔢 Classifica Risultati Esatti")
    res_dict = {f"{i}-{j}": matrice[i, j] for i in range(4) for j in range(4)}
    top_ris = sorted(res_dict.items(), key=lambda x: x[1], reverse=True)[:3]
    tr1, tr2, tr3 = st.columns(3)
    cols_tr = [tr1, tr2, tr3]
    for idx, (score, prob) in enumerate(top_ris):
        cols_tr[idx].markdown(f"<div class='neon-box' style='border-color:#00ffcc;'><div class='m-title'>Punteggio {score}</div><div class='m-value' style='color:#00ffcc;'>{prob*100:.1f}%</div><div class='m-quota'>Fair: {1/prob:.2f}</div></div>", unsafe_allow_html=True)