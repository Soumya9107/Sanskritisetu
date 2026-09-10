import json
import os
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler

PORT = 8000


def build_reply(message: str) -> str:
    user_query = (message or "").lower()

    heritage_replies = {
        "taj": "The Taj Mahal in Agra is a 17th-century marble mausoleum commissioned by Shah Jahan. Its symmetry, pietra dura inlay, calligraphy, and changing light make it a landmark of Mughal architecture and memory.",
        "hampi": "Hampi in Karnataka preserves the monumental landscape of the Vijayanagara Empire. Temple complexes, bazaars, boulders, and water systems reveal a sophisticated historic city shaped by trade, faith, and urban planning.",
        "qutub": "Qutub Minar in Delhi is a UNESCO World Heritage Site and a major example of early Indo-Islamic architecture. Its carved sandstone surfaces and surrounding complex record layers of Delhi Sultanate history.",
        "golden": "The Golden Temple, or Harmandir Sahib, in Amritsar is a spiritual and architectural center of Sikh heritage. Its reflection pool, gilded sanctum, and langar tradition express devotion, equality, and community service.",
        "warli": "Warli art is a living tribal mural tradition from Maharashtra. Simple geometric figures describe farming, weddings, dance, animals, and community life, creating a visual record of relationships with nature.",
        "victoria": "Victoria Memorial in Kolkata is an early-20th-century marble museum and memorial built in the Indo-Saracenic style. Its galleries and gardens preserve layers of Kolkata's colonial and artistic history.",
        "howrah": "Howrah Bridge, now called Rabindra Setu, is a historic cantilever bridge over the Hooghly River. Opened in 1943, it remains one of Kolkata's defining examples of engineering and urban heritage.",
        "indian museum": "The Indian Museum in Kolkata, established in 1814, is India's oldest and largest multipurpose museum. Its collections cover archaeology, art, anthropology, geology, and natural history.",
        "marble palace": "Marble Palace is a nineteenth-century mansion in North Kolkata known for its neoclassical architecture, sculpture, paintings, and eclectic private collection.",
        "bishnupur": "Bishnupur's terracotta temples in Bankura were built largely under the Malla rulers. Their fired-clay panels depict epics, musicians, animals, and everyday life in remarkable detail.",
        "hazarduari": "Hazarduari Palace in Murshidabad is a nineteenth-century palace beside the Bhagirathi River. Its name means 'a thousand doors', and the building now preserves historic collections and Nawabi-era memory.",
        "darjeeling": "The Darjeeling Himalayan Railway is a UNESCO World Heritage mountain railway opened in 1881. Its narrow-gauge route links the foothills with Darjeeling and reflects exceptional Himalayan engineering.",
        "sundarbans": "The Sundarbans are a UNESCO-listed mangrove landscape shaped by tides, waterways, and the Ganges-Brahmaputra delta. The region is also important habitat for the Royal Bengal tiger and local communities.",
        "santiniketan": "Santiniketan in Birbhum grew around Rabindranath Tagore's educational and cultural vision. Its open-air learning, arts practice, and Visva-Bharati tradition form a distinctive living heritage landscape.",
        "belur": "Belur Math on the Hooghly River is the headquarters of the Ramakrishna Math and Mission. Its architecture brings together Hindu, Islamic, and Christian visual influences in a message of religious harmony.",
        "kalighat": "Kalighat Temple in Kolkata is a major Shakti pilgrimage site dedicated to Goddess Kali. It also lends its name to Kalighat painting, a lively nineteenth-century urban folk-art tradition.",
        "kutch": "Kutch embroidery is a richly detailed textile tradition from Gujarat, known for mirror work, bold threads, geometric motifs, and the knowledge carried by artisan communities.",
        "channapatna": "Channapatna toys are turned wooden toys from Karnataka, traditionally finished with bright colors and natural lacquer. The craft is known for careful handwork and sustainable local materials.",
        "pashmina": "Kashmiri Pashmina is a fine mountain-wool textile made through hand-spinning, weaving, and embroidery. Its softness and detailed craftsmanship have made it an important part of Kashmir's living textile heritage.",
    }

    for keyword, reply in heritage_replies.items():
        if keyword in user_query or (keyword == "taj" and "tajmahal" in user_query):
            return reply
    if "madhubani" in user_query:
        return "Madhubani art originates from the Mithila region of Bihar. It is characterized by geometric patterns and vibrant natural dyes representing themes of nature and mythology."
    if "tanjore" in user_query:
        return "Tanjore painting is a classical South Indian painting style from Thanjavur, Tamil Nadu. It is famous for rich colors, gold foil overlays, and glass bead embellishments."
    if "konark" in user_query:
        return "The Konark Sun Temple in Odisha is a 13th-century UNESCO World Heritage Site designed in the shape of a massive stone chariot dedicated to the Sun God Surya."
    if "heritage" in user_query or "culture" in user_query or "india" in user_query:
        return f"I do not have a curated entry for '{message}' yet. Ask me about a specific monument, craft, festival, region, or tradition and I will share the heritage context available in this guide."
    return f"I could not identify a heritage topic in '{message}'. Try a specific name such as Konark, Hampi, Madhubani, Warli, or the Taj Mahal."


class HeritageHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def do_GET(self):
        if self.path == "/":
            self.path = "/index.html"
        return super().do_GET()

    def do_POST(self):
        if self.path == "/api/chat":
            length = int(self.headers.get("Content-Length", "0"))
            raw_data = self.rfile.read(length).decode("utf-8")

            try:
                payload = json.loads(raw_data or "{}")
            except json.JSONDecodeError:
                payload = {}

            message = str(payload.get("message", "")).strip()
            response = {"reply": build_reply(message)}

            body = json.dumps(response).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        self.send_response(404)
        self.end_headers()


if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    server = ThreadingHTTPServer(("127.0.0.1", PORT), HeritageHandler)
    print(f"SANSKRITISETU server running at http://127.0.0.1:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping SANSKRITISETU server...")
        server.server_close()