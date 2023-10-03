class PhRegPrv:
    def __init__(self):
        self.regions = {
            "NCR": [
                "NCR 1",
                "NCR 2",
                "NCR 3",
                "NCR 4",
                "NCR 5"
            ],
            "CAR": [
                "Abra",
                "Apayao",
                "Benguet",
                "Ifugao",
                "Kalinga",
                "Mountain Province"
            ],
            "Ilocos Region": [
                "Ilocos Norte",
                "Ilocos Sur",
                "La Union",
                "Pangasinan"
            ],
            "Cagayan Valley": [
                "Batanes",
                "Cagayan",
                "Isabela",
                "Nueva Vizcaya",
                "Quirino"
            ],
            "Central Luzon": [
                "Aurora",
                "Bataan",
                "Bulacan",
                "Nueva Ecija",
                "Pampanga",
                "Tarlac",
                "Zambales"
            ],
            "CALABARZON": [
                "Batangas",
                "Cavite",
                "Laguna",
                "Quezon",
                "Rizal"
            ],
            "MIMAROPA": [
                "Marinduque",
                "Occidental Mindoro",
                "Oriental Mindoro",
                "Palawan",
                "Romblon"
            ],
            "Bicol Region": [
                "Albay",
                "Camarines Norte",
                "Camarines Sur",
                "Catanduanes",
                "Masbate",
                "Sorsogon"
            ],
            "Western Visayas": [
                "Aklan",
                "Antique",
                "Capiz",
                "Guimaras",
                "Iloilo",
                "Negros Occidental"
            ],
            "Central Visayas": [
                "Bohol",
                "Cebu",
                "Negros Oriental",
                "Siquijor"
            ],
            "Eastern Visayas": [
                "Biliran",
                "Eastern Samar",
                "Leyte",
                "Northern Samar",
                "Samar",
                "Southern Leyte"
            ],
            "Zamboanga Peninsula": [
                "Zamboanga del Norte",
                "Zamboanga del Sur",
                "Zamboanga Sibugay"
            ],
            "Northern Mindanao": [
                "Bukidnon",
                "Camiguin",
                "Lanao del Norte",
                "Misamis Occidental",
                "Misamis Oriental"
            ],
            "Davao Region": [
                "Davao de Oro",
                "Davao del Norte",
                "Davao del Sur",
                "Davao Occidental",
                "Davao Oriental"
            ],
            "SOCCSKSARGEN": [
                "Cotabato",
                "Sarangani",
                "South Cotabato",
                "Sultan Kudarat"
            ],
            "Caraga": [
                "Agusan del Norte",
                "Agusan del Sur",
                "Dinagat Islands",
                "Surigao del Norte",
                "Surigao del Sur",
            ],
            "BARMM": [
                "Basilan",
                "Lanao del Sur",
                "Maguindanao",
                "Sulu",
                "Tawi-Tawi",
                "Eight Area Cluster"
            ]
        }

    def get_regions(self):
        return list(self.regions.keys())

    def get_provinces(self, region):
        if region in self.regions:
            return self.regions[region]
        else:
            return []
