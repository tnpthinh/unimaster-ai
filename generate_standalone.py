import sys
import server

print("Generating offline standalone HTML...")
html_str = server.generate_standalone_html_string()
out_path = r'UniMaster_Chay_Moi_Noi_Khong_Can_PC.html'

with open(out_path, 'w', encoding='utf-8') as f:
    f.write(html_str)

print(f"Generated standalone HTML successfully. Size: {len(html_str):,} bytes.")
