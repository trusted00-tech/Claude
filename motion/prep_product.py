"""python3 prep_product.py <shopify-handle> [store=https://orora.co.id]
Download product images from the Shopify store into assets/<handle>/, clean baked-in listing text
(logo top-left, title top-right, icon column left) with inpainting -> clean_N.jpg, and save product.json."""
import json, os, sys, urllib.request, cv2, numpy as np
h = sys.argv[1]; store = sys.argv[2] if len(sys.argv) > 2 else 'https://orora.co.id'
d = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', h); os.makedirs(d, exist_ok=True)
p = json.load(urllib.request.urlopen(f'{store}/products/{h}.json'))['product']
json.dump(p, open(f'{d}/product.json', 'w'))
for i, im in enumerate(p['images']):
    raw = f'{d}/img{i}.jpg'; urllib.request.urlretrieve(im['src'], raw)
    a = cv2.imread(raw); H, W = a.shape[:2]; m = np.zeros((H, W), np.uint8)
    sx, sy = W / 1024, H / 1024
    m[0:int(150*sy), int(700*sx):W] = 255; m[0:int(150*sy), 0:int(160*sx)] = 255; m[int(340*sy):H, 0:int(140*sx)] = 255
    cv2.imwrite(f'{d}/clean{i}.jpg', cv2.inpaint(a, m, 9, cv2.INPAINT_TELEA), [cv2.IMWRITE_JPEG_QUALITY, 95])
print(f"{len(p['images'])} images -> {d}  (raw imgN.jpg for infographics/CTA, cleanN.jpg for model photos)")
