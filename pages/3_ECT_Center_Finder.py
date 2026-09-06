import streamlit as st
from pathlib import Path
import json, math, urllib.request

st.markdown("<div style='height:1.45rem'></div>", unsafe_allow_html=True)
st.markdown("<div style='font-size:1.55rem;line-height:1.08;font-weight:700;margin:.1rem 0 .15rem;color:#356fa8'>⚡ ECT Center Finder</div>", unsafe_allow_html=True)
st.write("Find veterinary centers offering electrochemotherapy (ECT) in the USA and Canada.")

CENTERS=json.loads((Path(__file__).resolve().parents[1]/"data"/"ect_centers_usa_canada.json").read_text())["centers"]
CITY_COORDS={
("Toronto","ON"):(43.6532,-79.3832),("Brossard","QC"):(45.4501,-73.4658),("Auburn","AL"):(32.6099,-85.4808),("Laguna Hills","CA"):(33.6125,-117.7128),("Los Angeles","CA"):(34.0522,-118.2437),("San Francisco","CA"):(37.7749,-122.4194),("Boulder","CO"):(40.0150,-105.2705),("Colorado Springs","CO"):(38.8339,-104.8214),("Lafayette","CO"):(39.9936,-105.0897),("Lakewood","CO"):(39.7047,-105.0814),("Boca Raton","FL"):(26.3683,-80.1289),("Coral Springs","FL"):(26.2712,-80.2706),("Gainesville","FL"):(29.6516,-82.3248),("Melbourne","FL"):(28.0836,-80.6081),("Marietta","GA"):(33.9526,-84.5499),("Savannah","GA"):(32.0809,-81.0912),("Buzzards Bay","MA"):(41.7454,-70.6181),("South Weymouth","MA"):(42.1751,-70.9495),("Walpole","MA"):(42.1418,-71.2495),("Rockville","MD"):(39.0840,-77.1528),("Auburn Hills","MI"):(42.6875,-83.2341),("Bloomfield Hills","MI"):(42.5836,-83.2455),("Arden Hills","MN"):(45.0502,-93.1566),("Oakdale","MN"):(44.9630,-92.9649),("Raleigh","NC"):(35.7796,-78.6382),("Stratham","NH"):(43.0231,-70.9137),("Eatontown","NJ"):(40.2962,-74.0509),("Woodbridge","NJ"):(40.5576,-74.2846),("Santa Fe","NM"):(35.6870,-105.9378),("New York","NY"):(40.7128,-74.0060),("Bend","OR"):(44.0582,-121.3153),("Milwaukie","OR"):(45.4462,-122.6393),("Tacoma","WA"):(47.2529,-122.4443),("Waukesha","WI"):(43.0117,-88.2315)}

def miles(a,b,c,d):
    r=3958.8;p1=math.radians(a);p2=math.radians(c);dp=math.radians(c-a);dl=math.radians(d-b)
    x=math.sin(dp/2)**2+math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return 2*r*math.asin(math.sqrt(x))

def zip_coords(z):
    for country in ("us","ca"):
        try:
            req=urllib.request.Request(f"https://api.zippopotam.us/{country}/{z}",headers={"User-Agent":"VetCancerTreatmentFinder/1.0"})
            with urllib.request.urlopen(req,timeout=5) as resp:data=json.load(resp)
            p=data["places"][0];return float(p["latitude"]),float(p["longitude"]),p.get("place name",""),p.get("state abbreviation",p.get("state",""))
        except Exception:pass
    return None

zip_code=st.text_input("ZIP / postal code",placeholder="e.g. 01095 or M5V 3L9")
if st.button("Find nearest ECT centers",use_container_width=True):
    z=zip_code.strip().replace(" ","")
    loc=zip_coords(z)
    if not loc:st.error("ZIP / postal code not found. Try a valid US ZIP or Canadian postal code.")
    else:
        lat,lon,place,region=loc
        ranked=[]
        for x in CENTERS:
            coord=CITY_COORDS.get((x["city"],x["region"]))
            if coord:ranked.append((miles(lat,lon,*coord),x))
        ranked.sort(key=lambda v:v[0])
        st.success(f"Nearest listed ECT centers to {place}{', '+region if region else ''}")
        for dist,x in ranked[:8]:
            with st.container(border=True):
                st.subheader(x["center"])
                st.write(f"{x['city']}, {x['region']} · approximately {dist:.0f} miles away")
                st.markdown(f"☎️ [{x['phone']}](tel:{x['phone'].replace('-', '')})")
                st.link_button("Center website",x["website"],use_container_width=True)
        st.caption("Distances are straight-line estimates from the entered postal code to the center city, not driving distances. Confirm that ECT is currently available before travel.")
