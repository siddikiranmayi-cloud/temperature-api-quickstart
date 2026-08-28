import streamlit as st
import requests
import time
import folium
from streamlit_folium import st_folium

st.set_page_config(
    page_title="FortyGuard Heat Analysis",
    page_icon="🌡️",
    layout="wide"
                
)
st.title("🛰️ FortyGuard Heat Analysis")

st.write(
    "Generate a real heatmap using the FortyGuard API."
)
st.sidebar.header("🔑 API Settings")

api_key = st.sidebar.text_input(
    "FortyGuard API Key",
    type="password"
)
st.sidebar.header("📍 Location")

latitude = st.sidebar.number_input(
    "Latitude",
    value=40.7128,
    format="%.6f"
)

longitude = st.sidebar.number_input(
    "Longitude",
    value=-74.0060,
    format="%.6f"
)
# =========================================================
# HEATMAP BUTTON & STATE
# =========================================================

# Initialize memory so map doesn't disappear when clicked
if "final_result" not in st.session_state:
    st.session_state.final_result = None

generate_heatmap = st.button(
    "🗺️ Generate Real Heatmap",
    use_container_width=True
)

def create_polygon(lat, lon):

    size = 0.01

    polygon = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                        "properties": {},
                        "geometry": {
                            "type":
"Polygon",
                            "coordinates": [
                                [
                                    [
                                        lon - size,
                                        lat - size
                                    ],
                                    [
                                        lon + size,
                                        lat - size
                                    ],
                                    [
                                        lon + size,
                                        lat + size
                                    ],
                                    [                                                                                                                                                                                                                                                                                                                                           
                                        lon - size,
                                        lat + size
                                    ],                                                                                                                                                                                                                                                                                                                                                                                                                                      
                                    [                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
                                        lon - size,
                                        lat - size
                                    ]
                                ]
                            ]
                    }
            }
        ]
    }
    return polygon
if generate_heatmap:
    if not api_key:

        st.error(
            "❌ Please enter your FortyGuard API key."
        )

        st.stop()
    polygon = create_polygon(
        latitude,
        longitude
                            
    )
    current_date = time.strftime(
        "%Y-%m-%d"
                    
    )
    payload = {

        "polygon_aoi": polygon,

        "date_time": {

            "start_date": 
current_date,

            "start_time": "14:00",

            "filter_type": 1

        },

        "granularity": 100
                                                                                
    
    }
    headers = {

        "api-key": api_key,

        "Content-Type": "application/json"

                            
    }
    st.info(
        "🚀 Sending heatmap request to FortyGuard..."
    )

    try:

        response = requests.post(
"https://api.fortyguard.com/v1/heatmap",

            headers=headers,

            json=payload,

            timeout=60
        )                                                       


    except requests.exceptions.RequestException as error:

        st.error(
            f"❌ Connection error: {st.error}"
                                                                                                    
        )
        st.stop()
    if response.status_code != 200:

        st.error(
            f"❌ API Error: {response.status_code}"
        )

        st.code(
            response.text
        )                                                        

        st.stop()
    result = response.json()

    activity_id = result["data"]["activity_id"]


    st.success(
        "✅ Heatmap request submitted!"
    )


    st.write(
        f"Activity ID: `{activity_id}`"
    )
    status_url = f"https://api.fortyguard.com/v1/status/{activity_id}"

    progress = st.progress(0)
                
    # Placeholder so text updates in-place instead of printing 120 lines
    status_container = st.empty()
    status_container.info("⏳ Waiting for FortyGuard to generate the heatmap...")

    for attempt in range(120):

        try:
            status_response = requests.get(
                status_url,
                headers={"api-key": api_key},
                timeout=30
            )
        except requests.exceptions.RequestException as error:
            st.error(f"❌ Status request error: {error}")
            st.stop()

        if status_response.status_code != 200:
            st.error("❌ Could not check heatmap status.")
            st.code(status_response.text)
            st.stop()

        status_json = status_response.json()
        data = status_json.get("data", {})
        status = data.get("status", "")

                                                                                                                                                                                                                                        
        status_container.write(f"Current status: **{status}** (Checking... attempt {attempt + 1}/120)")

                                                                                                                                                                                                                                                        
        if status.lower() == "completed":
            st.session_state.final_result = data.get("result")
            progress.progress(100)
            status_container.success("🎉 Heatmap generated successfully!")
        break

                                                                                                                                                                                                                                                                                                                        
        if status.lower() == "failed":
            status_container.error("❌ FortyGuard heatmap generation failed.")
            st.json(data)
            st.stop()

        progress.progress(min((attempt + 1) / 120, 0.99))
        time.sleep(5)
                                                                                                                                                                                                                                                                                                                                            
    # =========================================================
    # STEP 3: DISPLAY HEATMAP (Out of button block for persistence)
    # =========================================================

    # Wrap ALL display logic inside the session_state check
    if st.session_state.final_result:

        final_result = st.session_state.final_result
        map_data = final_result.get("map_data")
        stats_data = final_result.get("stats_data")

        st.header("🔥 Real FortyGuard Heatmap")

        heatmap_map = folium.Map(
            location=[latitude, longitude],
            zoom_start=13
        )

        if map_data:
            folium.GeoJson(
                map_data,
                name="FortyGuard Heatmap"
            ).add_to(heatmap_map)
        else:
            st.warning("⚠️ No map data was returned by FortyGuard.")

        folium.Marker(
            [latitude, longitude],
            popup="Selected Location",
            tooltip="Heatmap Location"
        ).add_to(heatmap_map)

        st_folium(
            heatmap_map,
            width=1200,
            height=650
        )
        if stats_data:
            st.header("🌡️ Temperature Statistics")

            temperature_stats = stats_data.get("temperature_stats", {})

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Minimum Temperature", f"{temperature_stats.get('minimum', 'N/A')} °C")

            with col2:
                st.metric("Maximum Temperature", f"{temperature_stats.get('maximum', 'N/A')} °C")

            with col3:
                st.metric("Average Temperature", f"{temperature_stats.get('mean', 'N/A')} °C")

            st.subheader("📊 Heatmap Data")
            st.json(stats_data)
                                                                                                                                                                                                                                                            

    st.header(
        "🔥 Real FortyGuard Heatmap"
    )

    map_data = None
    stats_data = None

    # Send request to FortyGuard
    response = requests.post(...)

    if response.ok:
        final_result= response.json()

    map_data = final_result.get("map_data")
    stats_data = final_result.get("stats_data")

    st.success("✅ Heatmap generated successfully!")
    map_data = None

    if map_data:
        st.json(map_data)
    else:
        st.warning("No map data returned by FortyGuard.")
else:
    st.error(
        f"API Error: 
    {response.status_code}"
f"{response.text}"
    )
map_obj = folium.Map(

        location=[
            latitude,
            longitude
        ],

        zoom_start=13
    )   
map_data = None
if map_data:

        folium.GeoJson(

            map_data,

            name="FortyGuard Heatmap"

        ).add_to(
            heatmap_map
        )

else:

        st.warning(
            "⚠️ No map data was returned by FortyGuard."
        )
        folium.Marker(

        [
            latitude,
            longitude
        ],

        popup="Selected Location",

        tooltip="Heatmap Location"

    ).add_to(
        heatmap_map
    )
        st_folium(

        heatmap_map,

        width=1200,

        height=650
    )
if stats_data:

        st.header(
            "🌡️ Temperature Statistics"
        )


        temperature_stats = stats_data.get(

            "temperature_stats",

            {}
        )


        col1, col2, col3 = st.columns(3)
        with col1:

            st.metric(

                "Minimum Temperature",

f"{temperature_stats.get('minimum', 'N/A')} °C"
            )
        with col2:

            st.metric(

                "Maximum Temperature",

f"{temperature_stats.get('maximum', 'N/A')} °C"
            )
        with col3:

            st.metric(

                "Average Temperature",

f"{temperature_stats.get('mean', 'N/A')} °C"
            )
        st.subheader(
            "📊 Heatmap Data"
        )

        st.json(
            stats_data
        )
        
                    



            

                                
                    

    



                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
