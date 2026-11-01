from pathlib import Path
from io import BytesIO
import requests, cairosvg
from PIL import Image

logos = {
  "disney-plus": "https://commons.wikimedia.org/wiki/Special:FilePath/Disney%2B_logo.svg",
  "sl-benfica": "https://raw.githubusercontent.com/JoseArroyave/football-logos/main/logos/portugal/Benfica.svg",
  "unesco": "https://commons.wikimedia.org/wiki/Special:FilePath/UNESCO_logo.svg",
  "sporting-cp": "https://raw.githubusercontent.com/JoseArroyave/football-logos/main/logos/portugal/Sporting_CP.svg",
  "fc-porto": "https://raw.githubusercontent.com/JoseArroyave/football-logos/main/logos/portugal/FC_Porto.svg",
  "fifa": "https://raw.githubusercontent.com/simple-icons/simple-icons/develop/icons/fifa.svg",
  "formula-1": "https://commons.wikimedia.org/wiki/Special:FilePath/Formula_One_logo.svg",
  "rock-in-rio": "https://www.google.com/s2/favicons?domain=rockinrio.com&sz=256"
}
output=Path("Index/clients")
output.mkdir(parents=True,exist_ok=True)
for name,url in logos.items():
    response=requests.get(url,timeout=40,headers={"User-Agent":"BrunoCarinhasPortfolio/1.0 (logo assets)"})
    response.raise_for_status()
    data=response.content
    if data[:200].lstrip().startswith(b"<svg") or b"<svg" in data[:500]:
        data=cairosvg.svg2png(bytestring=data,output_width=750)
    image=Image.open(BytesIO(data)).convert("RGBA")
    alpha=image.getchannel("A")
    bounds=alpha.getbbox()
    if not bounds: raise ValueError("Empty image: "+name)
    alpha=alpha.crop(bounds)
    width,height=alpha.size
    result=Image.new("RGBA",(width,height),(255,255,255,0))
    result.putalpha(alpha)
    result.thumbnail((900,420),Image.Resampling.LANCZOS)
    target=output/(name+"-white.png")
    result.save(target,optimize=True)
    print(name,result.size,target.stat().st_size)
