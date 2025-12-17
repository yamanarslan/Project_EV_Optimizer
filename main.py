import networkx as nx
import matplotlib.pyplot as plt

# --- EV (ELEKTRİKLİ ARAÇ) AYARLARI ---
# Aracın dolu şarjla gidebileceği maksimum yol (KM)
MAX_RANGE_KM = 300 
# Şehirler ve Aralarındaki Mesafeler (KM)
# Bu veriler bir Graph (Çizge) yapısı oluşturur.
locations = {
    'Izmir': (0, 0),
    'Manisa': (1, 1),
    'Susurluk_Sarj': (3, 4), # Şarj İstasyonu
    'Bursa': (4, 6),
    'Gebze_Sarj': (5, 8),    # Şarj İstasyonu
    'Istanbul': (6, 9),
    'Canakkale': (0, 6),
    'Balikesir': (2, 3),
    'Aydin': (0, -2),
    'Mugla': (1, -4)
}

# Yollar (Başlangıç, Bitiş, Mesafe KM)
roads = [
    ('Izmir', 'Manisa', 40),
    ('Izmir', 'Aydin', 110),
    ('Aydin', 'Mugla', 100),
    ('Izmir', 'Canakkale', 320),
    ('Manisa', 'Balikesir', 140),
    ('Balikesir', 'Susurluk_Sarj', 50),
    ('Susurluk_Sarj', 'Bursa', 110),
    ('Bursa', 'Gebze_Sarj', 90),
    ('Gebze_Sarj', 'Istanbul', 60),
    ('Canakkale', 'Bursa', 270)
]

# --- ALGORİTMA KISMI (Graph Theory) ---
def find_best_route(start, end):
    # 1. Grafiği Oluştur
    G = nx.Graph()
    for s, e, dist in roads:
        G.add_edge(s, e, weight=dist)
    
    try:
        # 2. Dijkstra Algoritması ile En Kısa Yolu Bul
        path = nx.dijkstra_path(G, start, end, weight='weight')
        
        # 3. Toplam Mesafeyi Hesapla
        total_dist = 0
        path_edges = []
        
        print(f"\n--- ROTING: {start} -> {end} ---")
        for i in range(len(path)-1):
            u = path[i]
            v = path[i+1]
            dist = G[u][v]['weight']
            total_dist += dist
            path_edges.append((u, v))
            print(f"Segment: {u} -> {v} ({dist} km)")
            
        print(f"TOPLAM MESAFE: {total_dist} km")
        
        # 4. Batarya Kontrolü
        status_color = 'green'
        if total_dist > MAX_RANGE_KM:
            print(f"⚠️ UYARI: Menzil Yetersiz! ({total_dist} > {MAX_RANGE_KM})")
            print("   -> Lütfen rotadaki Şarj İstasyonlarını kullanın.")
            status_color = 'orange' # Riskli rota rengi
        else:
            print("✅ BAŞARILI: Mevcut şarj ile varış noktasına ulaşılabilir.")
        
        return G, path, path_edges, status_color

    except nx.NetworkXNoPath:
        print("HATA: Bu iki şehir arasında yol yok!")
        return G, [], [], 'red'

# --- GÖRSELLEŞTİRME KISMI ---
def draw_map(G, path, path_edges, color):
    plt.figure(figsize=(10, 8))
    
    # Düğümlerin konumlarını al
    pos = locations
    
    # 1. Tüm yolları gri çiz
    nx.draw_networkx_edges(G, pos, edge_color='lightgray', width=2)
    
    # 2. Şehirleri mavi çiz
    nx.draw_networkx_nodes(G, pos, node_size=1000, node_color='skyblue')
    
    # 3. İsimleri yaz
    nx.draw_networkx_labels(G, pos, font_size=9, font_weight='bold')
    
    # 4. Mesafeleri yolların üzerine yaz
    edge_labels = nx.get_edge_attributes(G, 'weight')
    labels_formatted = {k: f"{v}km" for k, v in edge_labels.items()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels_formatted, font_size=8)
    
    # 5. SEÇİLEN ROTAYI RENKLİ ÇİZ
    if path:
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color=color, width=4)
        nx.draw_networkx_nodes(G, pos, nodelist=path, node_color=color, node_size=1100)
    
    plt.title(f"EV Route Planner (Range: {MAX_RANGE_KM}km)", fontsize=14)
    plt.axis('off')
    plt.show()

# --- SİMÜLASYONU BAŞLAT ---
# İzmir'den İstanbul'a rota planla
my_graph, my_path, my_edges, my_color = find_best_route('Izmir', 'Istanbul')

# Haritayı Çiz
draw_map(my_graph, my_path, my_edges, my_color)