import streamlit as st
import requests
import json

API_BASE = "http://localhost:8000/api"

st.set_page_config(page_title="Pokemon MCP Server", layout="wide")
st.title("🔥 Pokemon MCP Server Interface")

tab1, tab2, tab3, tab4 = st.tabs(["Search Pokemon", "Compare Pokemon", "Strategy", "Team Builder"])

with tab1:
    st.header("Search Pokemon")
    pokemon_name = st.text_input("Enter Pokemon name:")
    if st.button("Search"):
        if pokemon_name:
            try:
                response = requests.get(f"{API_BASE}/pokemon/{pokemon_name}/")
                if response.status_code == 200:
                    data = response.json()
                    col1, col2 = st.columns(2)
                    with col1:
                        st.subheader(f"{data['name'].title()}")
                        st.write(f"**ID:** {data['id']}")
                        st.write(f"**Height:** {data['height']}")
                        st.write(f"**Weight:** {data['weight']}")
                        st.write(f"**Types:** {', '.join(data['types'])}")
                    with col2:
                        st.subheader("Stats")
                        for stat, value in data['stats'].items():
                            st.write(f"**{stat.title()}:** {value}")
                        st.subheader("Abilities")
                        st.write(', '.join(data['abilities']))
                else:
                    st.error("Pokemon not found!")
            except Exception as e:
                st.error(f"Error: {str(e)}")
with tab2:
    st.header("Compare Pokemon")
    col1, col2 = st.columns(2)
    with col1:
        pokemon1 = st.text_input("First Pokemon:")
    with col2:
        pokemon2 = st.text_input("Second Pokemon:")
    
    if st.button("Compare"):
        if pokemon1 and pokemon2:
            try:
                response = requests.post(f"{API_BASE}/compare/", 
                                       json={"pokemon1": pokemon1, "pokemon2": pokemon2})
                if response.status_code == 200:
                    data = response.json()
                    st.subheader("🤖 AI-Powered Comparison Results")
                    
                    st.write(f"**Battle:** {data['pokemon_1'].title()} vs {data['pokemon_2'].title()}")
                    
                    if data['winner'] != 'tie':
                        st.success(f"🏆 **Winner:** {data['winner'].title()}")
                    else:
                        st.info("🤝 **Result:** Tie")
                    
                    st.subheader("📊 Analysis")
                    st.write(f"**Summary:** {data['comparison_summary']}")
                    st.write(f"**Stats Analysis:** {data['stat_analysis']}")
                    st.write(f"**Type Matchup:** {data['type_advantage']}")
                    
                    st.subheader("💡 Recommendation")
                    st.write(data['recommendation'])
                    
                else:
                    st.error("Error comparing Pokemon!")
            except Exception as e:
                st.error(f"Error: {str(e)}")

with tab3:
    st.header("Strategy & Counters")
    pokemon_name = st.text_input("Pokemon to counter:")
    if st.button("Get Strategy"):
        if pokemon_name:
            try:
                response = requests.get(f"{API_BASE}/strategy/{pokemon_name}/")
                if response.status_code == 200:
                    data = response.json()
                    st.subheader(f"Counter Strategy for {data['pokemon'].title()}")
                    st.write(f"**Types:** {', '.join(data['types'])}")
                    
                    st.subheader("Top Weaknesses")
                    for weakness, value in data['top_weaknesses'].items():
                        st.write(f"**{weakness.title()}:** {value}x damage")
                    
                    st.subheader("Recommended Counters")
                    for counter in data['recommended_counters']:
                        st.write(f"• {counter.title()}")
                else:
                    st.error("Pokemon not found!")
            except Exception as e:
                st.error(f"Error: {str(e)}")

with tab4:
    st.header("Team Builder")
    team_description = st.text_area("Describe your ideal team:", 
                                   placeholder="e.g., balanced team with strong defense and fire attacker")
    if st.button("Generate Team"):
        if team_description:
            try:
                response = requests.post(f"{API_BASE}/team/", 
                                       json={"description": team_description})
                if response.status_code == 200:
                    data = response.json()
                    st.subheader("Generated Team")
                    st.write(f"**Strategy:** {data['description']}")
                    
                    st.subheader("Team Members")
                    for i, member in enumerate(data['team'], 1):
                        st.write(f"{i}. **{member['name'].title()}** - {member['role']}")
                else:
                    st.error("Error generating team!")
            except Exception as e:
                st.error(f"Error: {str(e)}")