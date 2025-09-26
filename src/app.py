import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"  # ton API FastAPI

# === Session persistante pour garder le cookie ===
if "api_session" not in st.session_state:
    st.session_state.api_session = requests.Session()

if "user_id" not in st.session_state:
    st.session_state.user_id = None

# === Auth ===
st.sidebar.header("🔑 Authentification")
choice = st.sidebar.radio("Action :", ["Connexion", "Inscription"])

username = st.sidebar.text_input("Nom d'utilisateur")
password = st.sidebar.text_input("Mot de passe", type="password")

if choice == "Inscription":
    if st.sidebar.button("Créer un compte"):
        res = st.session_state.api_session.post(
            f"{API_URL}/register",
            json={"username": username, "password": password}
        )
        if res.status_code == 200:
            st.success("✅ Compte créé, connecte-toi maintenant")
        else:
            st.error(res.json()["detail"])

if choice == "Connexion":
    if st.sidebar.button("Se connecter"):
        res = st.session_state.api_session.post(
            f"{API_URL}/login",
            json={"username": username, "password": password}
        )
        if res.status_code == 200:
            data = res.json()
            if "user_id" in data:
                st.session_state.user_id = data["user_id"]
                st.success(f"✅ Connecté en tant que {st.session_state.user_id}")
            else:
                st.error("Réponse inattendue de l'API")
        else:
            st.error(res.json().get("detail", "Erreur de connexion"))

# === App principale ===
st.title("📚 DocuAgent - Analyse de documents")

if st.session_state.user_id:
    st.subheader(f"Bienvenue {st.session_state.user_id} !")

    # === Upload fichier ===
    st.header("📤 Charger un document")
    uploaded_file = st.file_uploader("Choisis un fichier (PDF, TXT, MD)", type=["pdf", "txt", "md"])
    if uploaded_file is not None:
        files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
        res = st.session_state.api_session.post(
            f"{API_URL}/upload_file?user_id={st.session_state.user_id}", 
            files=files
        )
        if res.status_code == 200:
            st.success(f"✅ Fichier {uploaded_file.name} chargé")
            st.json(res.json())
        else:
            st.error(res.json()["detail"])

    # === Onglets pour les actions ===
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
        ["📝 Résumé", "🏷️ Classification", "🌍 Traduction", "🤖 Agent", "🗂️ Mémoire", "💬 Chat libre"]
    )

    # Résumé
    with tab1:
        st.subheader("Résumé du document")
        if st.button("Générer le résumé"):
            res = st.session_state.api_session.post(f"{API_URL}/doc_summary")
            data = res.json()
            if res.status_code == 200 and "summary" in data:
                st.success("✅ Résumé généré")
                st.write(data["summary"])   
            else:
                st.error(data.get("detail", "Erreur inattendue"))
                st.json(data)

    # Classification
    with tab2:
        st.subheader("Classification du document")
        if st.button("Classifier le document"):
            res = st.session_state.api_session.post(f"{API_URL}/doc_classify")
            data = res.json()
            if res.status_code == 200 and "category" in data:
                st.success("✅ Classification réussie")
                st.markdown(f"**Catégorie :** {data['category']}")
                st.markdown(f"**Confiance :** {round(data['confidence']*100, 2)} %")
            else:
                st.error(data.get("detail", "Erreur inattendue"))
                st.json(data)  


    # Traduction
    with tab3:
        st.subheader("Traduction du résumé")
        if st.button("Traduire"):
            res = st.session_state.api_session.post(f"{API_URL}/doc_translate?user_id={st.session_state.user_id}") 
            data = res.json()
            if res.status_code == 200:
                st.success("✅ Traduction générée")
                st.write(data["translated"])
            else:
                st.error(data.get("detail", "Erreur inattendue"))
                st.json(data)  

    # Agent
    with tab4:
        st.subheader("Interroger l’agent")
        query = st.text_area("Pose ta question")
        if st.button("Envoyer"):
            res = st.session_state.api_session.post(f"{API_URL}/agent", json={"query": query})
            data = res.json()
            if res.status_code == 200:
                if data.get("response"):
                    st.success("✅ Réponse de l’agent")
                    st.write(data["response"])
                else:
                    st.warning("⚠️ Aucun résultat trouvé dans le document.")
            else:
                st.error(data.get("detail", "Erreur inattendue"))
                st.json(data)
    
    # Mémoire
    with tab5:
        st.subheader("🗂️ Historique de la mémoire")
        if st.button("Afficher l'historique"):
            res = st.session_state.api_session.get(f"{API_URL}/history")
            data = res.json()
            if res.status_code == 200:
                st.success(f"Historique de {data['user_id']}")
                for msg in data["messages"]:
                    role = msg["type"]
                    content = msg["content"]
                    st.markdown(f"**{role}:** {content}")
            else:
                st.error(data.get("detail", "Erreur inattendue"))
                st.json(data)

    # Chat libre
    with tab6:
        st.subheader("💬 Conversation libre avec le bot")
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        query = st.text_area("Ton message")
        if st.button("Envoyer au chat"):
            res = st.session_state.api_session.post(f"{API_URL}/chat", json={"query": query})
            data = res.json()
            if res.status_code == 200:
                response = data.get("response", "")
                st.session_state.chat_history.append(("👤", query))
                st.session_state.chat_history.append(("🤖", response))
                st.session_state.chat_input = ""
                st.rerun()

        # Affichage historique local
        if st.session_state.chat_history:
            st.subheader("Historique de la conversation")
            for role, content in st.session_state.chat_history:
                st.markdown(f"**{role}**: {content}")

else:
    st.info("🔒 Connecte-toi ou inscris-toi pour utiliser l’application.")
