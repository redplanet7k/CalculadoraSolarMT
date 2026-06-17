# -*- coding: utf-8 -*-
"""
dados_solar_mt.py — Irradiação Solar por Município do Mato Grosso
Fonte: Atlas Brasileiro de Energia Solar, 2ª Ed. — INPE/LABREN (2017)
       DOI: 10.34024/978851700089
Dados CSV: global_horizontal_means.csv (LABREN/INPE)
Método: IDW 4 vizinhos (grade 0,1°×0,1°) | 17 anos satélite GOES (1999-2015)
Validação Atlas: REQM≈8,2% | Viés≈0,2% (Tabela 4, p.42)
"""

DADOS_SOLAR_MT = {
    "Acorizal": {
        "lat": -15.2, "lon": -56.37,
        "global": 5.137,
        "mensal": {"Janeiro": 5.564, "Fevereiro": 5.507, "Março": 5.298, "Abril": 5.079, "Maio": 4.59, "Junho": 4.573, "Julho": 4.714, "Agosto": 5.567, "Setembro": 5.248, "Outubro": 5.437, "Novembro": 5.749, "Dezembro": 5.861},
    },
    "Alta Floresta": {
        "lat": -9.88, "lon": -56.09,
        "global": 5.25,
        "mensal": {"Janeiro": 4.911, "Fevereiro": 4.936, "Março": 4.784, "Abril": 4.678, "Maio": 4.681, "Junho": 4.806, "Julho": 4.921, "Agosto": 5.506, "Setembro": 5.242, "Outubro": 5.352, "Novembro": 5.124, "Dezembro": 5.099},
    },
    "Alto Araguaia": {
        "lat": -17.32, "lon": -53.22,
        "global": 5.16,
        "mensal": {"Janeiro": 5.615, "Fevereiro": 5.731, "Março": 5.282, "Abril": 5.23, "Maio": 4.752, "Junho": 4.513, "Julho": 4.652, "Agosto": 5.538, "Setembro": 5.448, "Outubro": 5.385, "Novembro": 5.562, "Dezembro": 5.759},
    },
    "Alto Boa Vista": {
        "lat": -10.87, "lon": -51.62,
        "global": 5.076,
        "mensal": {"Janeiro": 5.143, "Fevereiro": 5.265, "Março": 5.044, "Abril": 4.878, "Maio": 5.026, "Junho": 4.868, "Julho": 5.155, "Agosto": 5.75, "Setembro": 5.41, "Outubro": 5.34, "Novembro": 5.245, "Dezembro": 5.321},
    },
    "Alto Garças": {
        "lat": -16.94, "lon": -53.52,
        "global": 5.149,
        "mensal": {"Janeiro": 5.624, "Fevereiro": 5.665, "Março": 5.244, "Abril": 5.186, "Maio": 4.772, "Junho": 4.507, "Julho": 4.679, "Agosto": 5.49, "Setembro": 5.419, "Outubro": 5.404, "Novembro": 5.581, "Dezembro": 5.761},
    },
    "Alto Paraguai": {
        "lat": -14.51, "lon": -56.48,
        "global": 5.069,
        "mensal": {"Janeiro": 5.356, "Fevereiro": 5.312, "Março": 5.142, "Abril": 5.002, "Maio": 4.631, "Junho": 4.635, "Julho": 4.833, "Agosto": 5.617, "Setembro": 5.287, "Outubro": 5.383, "Novembro": 5.54, "Dezembro": 5.614},
    },
    "Alto Taquari": {
        "lat": -17.81, "lon": -53.28,
        "global": 5.062,
        "mensal": {"Janeiro": 5.549, "Fevereiro": 5.647, "Março": 5.199, "Abril": 5.031, "Maio": 4.612, "Junho": 4.382, "Julho": 4.545, "Agosto": 5.418, "Setembro": 5.34, "Outubro": 5.315, "Novembro": 5.489, "Dezembro": 5.744},
    },
    "Apiacás": {
        "lat": -9.54, "lon": -57.47,
        "global": 4.717,
        "mensal": {"Janeiro": 4.642, "Fevereiro": 4.667, "Março": 4.599, "Abril": 4.556, "Maio": 4.469, "Junho": 4.724, "Julho": 4.888, "Agosto": 5.352, "Setembro": 5.087, "Outubro": 5.188, "Novembro": 4.961, "Dezembro": 4.885},
    },
    "Araguaiana": {
        "lat": -15.73, "lon": -51.83,
        "global": 5.271,
        "mensal": {"Janeiro": 5.736, "Fevereiro": 5.868, "Março": 5.403, "Abril": 5.479, "Maio": 5.028, "Junho": 4.632, "Julho": 4.829, "Agosto": 5.414, "Setembro": 5.493, "Outubro": 5.664, "Novembro": 5.561, "Dezembro": 5.733},
    },
    "Araguainha": {
        "lat": -16.89, "lon": -52.61,
        "global": 5.215,
        "mensal": {"Janeiro": 5.712, "Fevereiro": 5.76, "Março": 5.405, "Abril": 5.278, "Maio": 4.872, "Junho": 4.504, "Julho": 4.603, "Agosto": 5.524, "Setembro": 5.483, "Outubro": 5.489, "Novembro": 5.684, "Dezembro": 5.839},
    },
    "Araputanga": {
        "lat": -15.47, "lon": -58.35,
        "global": 4.885,
        "mensal": {"Janeiro": 5.419, "Fevereiro": 5.213, "Março": 5.027, "Abril": 4.81, "Maio": 4.179, "Junho": 4.291, "Julho": 4.407, "Agosto": 5.23, "Setembro": 5.136, "Outubro": 5.298, "Novembro": 5.512, "Dezembro": 5.556},
    },
    "Arenápolis": {
        "lat": -14.44, "lon": -56.83,
        "global": 5.037,
        "mensal": {"Janeiro": 5.378, "Fevereiro": 5.306, "Março": 5.086, "Abril": 4.96, "Maio": 4.604, "Junho": 4.592, "Julho": 4.786, "Agosto": 5.53, "Setembro": 5.262, "Outubro": 5.386, "Novembro": 5.495, "Dezembro": 5.561},
    },
    "Aripuanã": {
        "lat": -9.17, "lon": -60.63,
        "global": 4.564,
        "mensal": {"Janeiro": 4.335, "Fevereiro": 4.399, "Março": 4.474, "Abril": 4.413, "Maio": 4.21, "Junho": 4.702, "Julho": 4.768, "Agosto": 5.142, "Setembro": 5.086, "Outubro": 5.178, "Novembro": 4.849, "Dezembro": 4.577},
    },
    "Barra do Bugres": {
        "lat": -15.07, "lon": -57.18,
        "global": 5.46,
        "mensal": {"Janeiro": 5.488, "Fevereiro": 5.39, "Março": 5.196, "Abril": 4.999, "Maio": 4.483, "Junho": 4.517, "Julho": 4.638, "Agosto": 5.34, "Setembro": 5.235, "Outubro": 5.445, "Novembro": 5.651, "Dezembro": 5.703},
    },
    "Barra do Garças": {
        "lat": -15.89, "lon": -52.26,
        "global": 5.51,
        "mensal": {"Janeiro": 5.61, "Fevereiro": 5.745, "Março": 5.332, "Abril": 5.429, "Maio": 5.066, "Junho": 4.698, "Julho": 4.839, "Agosto": 5.623, "Setembro": 5.426, "Outubro": 5.628, "Novembro": 5.565, "Dezembro": 5.685},
    },
    "Barão de Melgaço": {
        "lat": -16.19, "lon": -55.96,
        "global": 5.175,
        "mensal": {"Janeiro": 5.778, "Fevereiro": 5.698, "Março": 5.477, "Abril": 5.266, "Maio": 4.531, "Junho": 4.479, "Julho": 4.564, "Agosto": 5.564, "Setembro": 5.199, "Outubro": 5.45, "Novembro": 5.75, "Dezembro": 5.887},
    },
    "Bom Jesus do Araguaia": {
        "lat": -11.77, "lon": -51.75,
        "global": 5.097,
        "mensal": {"Janeiro": 5.098, "Fevereiro": 5.277, "Março": 5.009, "Abril": 4.91, "Maio": 5.031, "Junho": 4.964, "Julho": 5.356, "Agosto": 5.94, "Setembro": 5.408, "Outubro": 5.216, "Novembro": 5.225, "Dezembro": 5.252},
    },
    "Brasnorte": {
        "lat": -12.14, "lon": -58.01,
        "global": 4.898,
        "mensal": {"Janeiro": 5.021, "Fevereiro": 4.946, "Março": 4.902, "Abril": 4.854, "Maio": 4.646, "Junho": 4.651, "Julho": 4.802, "Agosto": 5.339, "Setembro": 5.186, "Outubro": 5.393, "Novembro": 5.194, "Dezembro": 5.307},
    },
    "Campinápolis": {
        "lat": -14.4, "lon": -52.84,
        "global": 5.295,
        "mensal": {"Janeiro": 5.589, "Fevereiro": 5.659, "Março": 5.423, "Abril": 5.467, "Maio": 5.124, "Junho": 4.853, "Julho": 5.189, "Agosto": 5.746, "Setembro": 5.465, "Outubro": 5.542, "Novembro": 5.472, "Dezembro": 5.598},
    },
    "Campo Novo do Parecis": {
        "lat": -13.67, "lon": -57.89,
        "global": 5.54,
        "mensal": {"Janeiro": 5.116, "Fevereiro": 5.082, "Março": 4.872, "Abril": 4.857, "Maio": 4.546, "Junho": 4.548, "Julho": 4.684, "Agosto": 5.352, "Setembro": 5.113, "Outubro": 5.258, "Novembro": 5.347, "Dezembro": 5.456},
    },
    "Campo Verde": {
        "lat": -15.55, "lon": -55.17,
        "global": 5.5,
        "mensal": {"Janeiro": 5.427, "Fevereiro": 5.282, "Março": 5.036, "Abril": 5.058, "Maio": 4.748, "Junho": 4.628, "Julho": 4.79, "Agosto": 5.57, "Setembro": 5.242, "Outubro": 5.203, "Novembro": 5.481, "Dezembro": 5.537},
    },
    "Campos de Júlio": {
        "lat": -13.53, "lon": -59.28,
        "global": 4.77,
        "mensal": {"Janeiro": 4.959, "Fevereiro": 4.823, "Março": 4.803, "Abril": 4.748, "Maio": 4.4, "Junho": 4.434, "Julho": 4.585, "Agosto": 5.09, "Setembro": 5.027, "Outubro": 5.205, "Novembro": 5.291, "Dezembro": 5.302},
    },
    "Canabrava do Norte": {
        "lat": -10.71, "lon": -51.87,
        "global": 5.098,
        "mensal": {"Janeiro": 5.206, "Fevereiro": 5.259, "Março": 5.051, "Abril": 4.899, "Maio": 5.014, "Junho": 5.023, "Julho": 5.203, "Agosto": 5.836, "Setembro": 5.374, "Outubro": 5.324, "Novembro": 5.215, "Dezembro": 5.301},
    },
    "Canarana": {
        "lat": -13.56, "lon": -52.27,
        "global": 5.229,
        "mensal": {"Janeiro": 5.471, "Fevereiro": 5.538, "Março": 5.209, "Abril": 5.282, "Maio": 5.044, "Junho": 4.885, "Julho": 5.3, "Agosto": 5.815, "Setembro": 5.493, "Outubro": 5.454, "Novembro": 5.305, "Dezembro": 5.525},
    },
    "Carlinda": {
        "lat": -9.98, "lon": -55.83,
        "global": 4.904,
        "mensal": {"Janeiro": 4.979, "Fevereiro": 4.94, "Março": 4.806, "Abril": 4.752, "Maio": 4.726, "Junho": 4.798, "Julho": 4.963, "Agosto": 5.484, "Setembro": 5.226, "Outubro": 5.333, "Novembro": 5.181, "Dezembro": 5.13},
    },
    "Castanheira": {
        "lat": -11.12, "lon": -58.3,
        "global": 4.822,
        "mensal": {"Janeiro": 4.765, "Fevereiro": 4.723, "Março": 4.71, "Abril": 4.703, "Maio": 4.543, "Junho": 4.749, "Julho": 4.928, "Agosto": 5.369, "Setembro": 5.216, "Outubro": 5.394, "Novembro": 5.135, "Dezembro": 5.073},
    },
    "Chapada dos Guimarães": {
        "lat": -15.46, "lon": -55.75,
        "global": 4.986,
        "mensal": {"Janeiro": 5.275, "Fevereiro": 5.172, "Março": 4.996, "Abril": 4.916, "Maio": 4.586, "Junho": 4.594, "Julho": 4.782, "Agosto": 5.613, "Setembro": 5.245, "Outubro": 5.252, "Novembro": 5.398, "Dezembro": 5.502},
    },
    "Cláudia": {
        "lat": -11.48, "lon": -54.88,
        "global": 5.013,
        "mensal": {"Janeiro": 5.164, "Fevereiro": 5.178, "Março": 4.99, "Abril": 4.986, "Maio": 4.865, "Junho": 4.782, "Julho": 5.153, "Agosto": 5.463, "Setembro": 5.264, "Outubro": 5.35, "Novembro": 5.229, "Dezembro": 5.235},
    },
    "Cocalinho": {
        "lat": -14.39, "lon": -51.0,
        "global": 5.293,
        "mensal": {"Janeiro": 5.6, "Fevereiro": 5.822, "Março": 5.452, "Abril": 5.419, "Maio": 5.028, "Junho": 4.701, "Julho": 5.091, "Agosto": 5.628, "Setembro": 5.629, "Outubro": 5.657, "Novembro": 5.494, "Dezembro": 5.577},
    },
    "Colniza": {
        "lat": -9.41, "lon": -59.54,
        "global": 4.63,
        "mensal": {"Janeiro": 4.497, "Fevereiro": 4.547, "Março": 4.511, "Abril": 4.435, "Maio": 4.313, "Junho": 4.732, "Julho": 4.813, "Agosto": 5.135, "Setembro": 5.06, "Outubro": 5.195, "Novembro": 5.02, "Dezembro": 4.702},
    },
    "Colíder": {
        "lat": -10.82, "lon": -55.45,
        "global": 5.42,
        "mensal": {"Janeiro": 5.118, "Fevereiro": 5.057, "Março": 4.932, "Abril": 4.852, "Maio": 4.785, "Junho": 4.797, "Julho": 5.106, "Agosto": 5.619, "Setembro": 5.263, "Outubro": 5.34, "Novembro": 5.218, "Dezembro": 5.185},
    },
    "Comodoro": {
        "lat": -13.66, "lon": -59.79,
        "global": 4.698,
        "mensal": {"Janeiro": 4.862, "Fevereiro": 4.65, "Março": 4.617, "Abril": 4.589, "Maio": 4.302, "Junho": 4.414, "Julho": 4.676, "Agosto": 5.173, "Setembro": 5.027, "Outubro": 5.185, "Novembro": 5.162, "Dezembro": 5.123},
    },
    "Confresa": {
        "lat": -10.64, "lon": -51.56,
        "global": 5.025,
        "mensal": {"Janeiro": 5.057, "Fevereiro": 5.153, "Março": 4.936, "Abril": 4.777, "Maio": 4.994, "Junho": 4.966, "Julho": 5.147, "Agosto": 5.793, "Setembro": 5.367, "Outubro": 5.241, "Novembro": 5.162, "Dezembro": 5.219},
    },
    "Conquista d'Oeste": {
        "lat": -13.52, "lon": -59.93,
        "global": 4.704,
        "mensal": {"Janeiro": 4.939, "Fevereiro": 4.645, "Março": 4.632, "Abril": 4.609, "Maio": 4.281, "Junho": 4.426, "Julho": 4.667, "Agosto": 5.175, "Setembro": 5.061, "Outubro": 5.196, "Novembro": 5.155, "Dezembro": 5.08},
    },
    "Cotriguaçu": {
        "lat": -9.86, "lon": -58.42,
        "global": 4.702,
        "mensal": {"Janeiro": 4.546, "Fevereiro": 4.633, "Março": 4.555, "Abril": 4.515, "Maio": 4.398, "Junho": 4.747, "Julho": 4.884, "Agosto": 5.334, "Setembro": 5.094, "Outubro": 5.257, "Novembro": 4.994, "Dezembro": 4.875},
    },
    "Cuiabá": {
        "lat": -15.6, "lon": -56.1,
        "global": 5.58,
        "mensal": {"Janeiro": 5.618, "Fevereiro": 5.491, "Março": 5.316, "Abril": 5.052, "Maio": 4.542, "Junho": 4.48, "Julho": 4.642, "Agosto": 5.543, "Setembro": 5.26, "Outubro": 5.446, "Novembro": 5.71, "Dezembro": 5.892},
    },
    "Curvelândia": {
        "lat": -15.99, "lon": -58.11,
        "global": 4.962,
        "mensal": {"Janeiro": 5.632, "Fevereiro": 5.411, "Março": 5.202, "Abril": 4.894, "Maio": 4.177, "Junho": 4.207, "Julho": 4.351, "Agosto": 5.12, "Setembro": 5.144, "Outubro": 5.443, "Novembro": 5.659, "Dezembro": 5.786},
    },
    "Cáceres": {
        "lat": -16.07, "lon": -57.68,
        "global": 5.52,
        "mensal": {"Janeiro": 5.675, "Fevereiro": 5.513, "Março": 5.298, "Abril": 4.974, "Maio": 4.346, "Junho": 4.342, "Julho": 4.458, "Agosto": 5.286, "Setembro": 5.26, "Outubro": 5.498, "Novembro": 5.73, "Dezembro": 5.85},
    },
    "Denise": {
        "lat": -14.73, "lon": -57.04,
        "global": 4.981,
        "mensal": {"Janeiro": 5.33, "Fevereiro": 5.339, "Março": 5.111, "Abril": 4.896, "Maio": 4.471, "Junho": 4.518, "Julho": 4.679, "Agosto": 5.379, "Setembro": 5.123, "Outubro": 5.349, "Novembro": 5.498, "Dezembro": 5.579},
    },
    "Diamantino": {
        "lat": -14.41, "lon": -56.45,
        "global": 5.56,
        "mensal": {"Janeiro": 5.37, "Fevereiro": 5.274, "Março": 5.067, "Abril": 4.97, "Maio": 4.671, "Junho": 4.629, "Julho": 4.846, "Agosto": 5.634, "Setembro": 5.288, "Outubro": 5.37, "Novembro": 5.436, "Dezembro": 5.589},
    },
    "Dom Aquino": {
        "lat": -15.8, "lon": -54.92,
        "global": 5.106,
        "mensal": {"Janeiro": 5.463, "Fevereiro": 5.397, "Março": 5.201, "Abril": 5.217, "Maio": 4.773, "Junho": 4.687, "Julho": 4.788, "Agosto": 5.733, "Setembro": 5.256, "Outubro": 5.218, "Novembro": 5.462, "Dezembro": 5.61},
    },
    "Feliz Natal": {
        "lat": -12.38, "lon": -54.93,
        "global": 5.092,
        "mensal": {"Janeiro": 5.261, "Fevereiro": 5.281, "Março": 5.109, "Abril": 5.112, "Maio": 5.039, "Junho": 4.845, "Julho": 5.13, "Agosto": 5.482, "Setembro": 5.293, "Outubro": 5.423, "Novembro": 5.271, "Dezembro": 5.378},
    },
    "Figueirópolis d'Oeste": {
        "lat": -15.36, "lon": -58.72,
        "global": 4.841,
        "mensal": {"Janeiro": 5.27, "Fevereiro": 5.091, "Março": 4.937, "Abril": 4.752, "Maio": 4.153, "Junho": 4.296, "Julho": 4.415, "Agosto": 5.197, "Setembro": 5.117, "Outubro": 5.3, "Novembro": 5.526, "Dezembro": 5.491},
    },
    "Gaúcha do Norte": {
        "lat": -13.19, "lon": -53.07,
        "global": 5.214,
        "mensal": {"Janeiro": 5.354, "Fevereiro": 5.552, "Março": 5.265, "Abril": 5.356, "Maio": 5.094, "Junho": 4.909, "Julho": 5.261, "Agosto": 5.735, "Setembro": 5.431, "Outubro": 5.42, "Novembro": 5.347, "Dezembro": 5.416},
    },
    "General Carneiro": {
        "lat": -15.69, "lon": -52.78,
        "global": 5.269,
        "mensal": {"Janeiro": 5.592, "Fevereiro": 5.704, "Março": 5.378, "Abril": 5.467, "Maio": 5.09, "Junho": 4.741, "Julho": 4.933, "Agosto": 5.655, "Setembro": 5.516, "Outubro": 5.567, "Novembro": 5.519, "Dezembro": 5.645},
    },
    "Glória d'Oeste": {
        "lat": -15.78, "lon": -58.29,
        "global": 4.968,
        "mensal": {"Janeiro": 5.556, "Fevereiro": 5.423, "Março": 5.163, "Abril": 4.892, "Maio": 4.197, "Junho": 4.243, "Julho": 4.396, "Agosto": 5.13, "Setembro": 5.18, "Outubro": 5.46, "Novembro": 5.67, "Dezembro": 5.792},
    },
    "Guarantã do Norte": {
        "lat": -9.79, "lon": -54.9,
        "global": 5.34,
        "mensal": {"Janeiro": 4.745, "Fevereiro": 4.769, "Março": 4.713, "Abril": 4.665, "Maio": 4.78, "Junho": 4.849, "Julho": 5.119, "Agosto": 5.695, "Setembro": 5.122, "Outubro": 5.102, "Novembro": 4.87, "Dezembro": 4.902},
    },
    "Guiratinga": {
        "lat": -16.35, "lon": -53.76,
        "global": 5.235,
        "mensal": {"Janeiro": 5.578, "Fevereiro": 5.625, "Março": 5.371, "Abril": 5.238, "Maio": 4.871, "Junho": 4.677, "Julho": 4.841, "Agosto": 5.71, "Setembro": 5.5, "Outubro": 5.525, "Novembro": 5.68, "Dezembro": 5.768},
    },
    "Indiavaí": {
        "lat": -15.49, "lon": -58.47,
        "global": 4.883,
        "mensal": {"Janeiro": 5.418, "Fevereiro": 5.219, "Março": 5.037, "Abril": 4.82, "Maio": 4.161, "Junho": 4.267, "Julho": 4.371, "Agosto": 5.205, "Setembro": 5.11, "Outubro": 5.335, "Novembro": 5.549, "Dezembro": 5.574},
    },
    "Ipiranga do Norte": {
        "lat": -12.17, "lon": -56.15,
        "global": 4.962,
        "mensal": {"Janeiro": 5.244, "Fevereiro": 5.109, "Março": 4.976, "Abril": 4.914, "Maio": 4.781, "Junho": 4.683, "Julho": 4.884, "Agosto": 5.345, "Setembro": 5.183, "Outubro": 5.365, "Novembro": 5.193, "Dezembro": 5.354},
    },
    "Itanhangá": {
        "lat": -12.15, "lon": -56.69,
        "global": 4.968,
        "mensal": {"Janeiro": 5.169, "Fevereiro": 4.984, "Março": 4.924, "Abril": 4.859, "Maio": 4.765, "Junho": 4.841, "Julho": 5.05, "Agosto": 5.483, "Setembro": 5.221, "Outubro": 5.399, "Novembro": 5.173, "Dezembro": 5.243},
    },
    "Itaúba": {
        "lat": -11.0, "lon": -55.34,
        "global": 4.944,
        "mensal": {"Janeiro": 5.055, "Fevereiro": 4.915, "Março": 4.842, "Abril": 4.789, "Maio": 4.797, "Junho": 4.901, "Julho": 5.241, "Agosto": 5.677, "Setembro": 5.2, "Outubro": 5.238, "Novembro": 5.091, "Dezembro": 5.057},
    },
    "Itiquira": {
        "lat": -17.21, "lon": -54.15,
        "global": 5.168,
        "mensal": {"Janeiro": 5.719, "Fevereiro": 5.65, "Março": 5.347, "Abril": 5.115, "Maio": 4.656, "Junho": 4.472, "Julho": 4.677, "Agosto": 5.541, "Setembro": 5.349, "Outubro": 5.407, "Novembro": 5.74, "Dezembro": 5.881},
    },
    "Jaciara": {
        "lat": -15.97, "lon": -54.97,
        "global": 5.109,
        "mensal": {"Janeiro": 5.481, "Fevereiro": 5.448, "Março": 5.211, "Abril": 5.216, "Maio": 4.754, "Junho": 4.649, "Julho": 4.746, "Agosto": 5.689, "Setembro": 5.281, "Outubro": 5.245, "Novembro": 5.511, "Dezembro": 5.607},
    },
    "Jangada": {
        "lat": -15.23, "lon": -56.47,
        "global": 5.127,
        "mensal": {"Janeiro": 5.541, "Fevereiro": 5.508, "Março": 5.297, "Abril": 5.066, "Maio": 4.591, "Junho": 4.576, "Julho": 4.715, "Agosto": 5.537, "Setembro": 5.257, "Outubro": 5.415, "Novembro": 5.723, "Dezembro": 5.829},
    },
    "Jauru": {
        "lat": -15.33, "lon": -58.16,
        "global": 4.818,
        "mensal": {"Janeiro": 5.2, "Fevereiro": 5.085, "Março": 4.911, "Abril": 4.774, "Maio": 4.222, "Junho": 4.342, "Julho": 4.467, "Agosto": 5.282, "Setembro": 5.067, "Outubro": 5.179, "Novembro": 5.393, "Dezembro": 5.339},
    },
    "Juara": {
        "lat": -11.27, "lon": -57.53,
        "global": 5.38,
        "mensal": {"Janeiro": 4.908, "Fevereiro": 4.879, "Março": 4.797, "Abril": 4.723, "Maio": 4.63, "Junho": 4.72, "Julho": 4.927, "Agosto": 5.37, "Setembro": 5.18, "Outubro": 5.359, "Novembro": 5.131, "Dezembro": 5.138},
    },
    "Juruena": {
        "lat": -10.33, "lon": -58.49,
        "global": 4.714,
        "mensal": {"Janeiro": 4.596, "Fevereiro": 4.644, "Março": 4.684, "Abril": 4.532, "Maio": 4.469, "Junho": 4.754, "Julho": 4.911, "Agosto": 5.272, "Setembro": 5.058, "Outubro": 5.286, "Novembro": 4.901, "Dezembro": 4.88},
    },
    "Juscimeira": {
        "lat": -16.05, "lon": -54.88,
        "global": 5.145,
        "mensal": {"Janeiro": 5.559, "Fevereiro": 5.554, "Março": 5.283, "Abril": 5.201, "Maio": 4.752, "Junho": 4.634, "Julho": 4.74, "Agosto": 5.702, "Setembro": 5.306, "Outubro": 5.298, "Novembro": 5.569, "Dezembro": 5.68},
    },
    "Juína": {
        "lat": -11.37, "lon": -58.7,
        "global": 5.31,
        "mensal": {"Janeiro": 4.74, "Fevereiro": 4.707, "Março": 4.723, "Abril": 4.639, "Maio": 4.485, "Junho": 4.667, "Julho": 4.821, "Agosto": 5.362, "Setembro": 5.121, "Outubro": 5.298, "Novembro": 5.023, "Dezembro": 5.117},
    },
    "Lambari d'Oeste": {
        "lat": -15.33, "lon": -58.0,
        "global": 4.897,
        "mensal": {"Janeiro": 5.289, "Fevereiro": 5.224, "Março": 5.081, "Abril": 4.836, "Maio": 4.31, "Junho": 4.379, "Julho": 4.491, "Agosto": 5.293, "Setembro": 5.134, "Outubro": 5.259, "Novembro": 5.453, "Dezembro": 5.479},
    },
    "Lucas do Rio Verde": {
        "lat": -13.05, "lon": -55.91,
        "global": 5.62,
        "mensal": {"Janeiro": 5.314, "Fevereiro": 5.111, "Março": 5.035, "Abril": 5.074, "Maio": 4.807, "Junho": 4.658, "Julho": 4.845, "Agosto": 5.3, "Setembro": 5.229, "Outubro": 5.375, "Novembro": 5.357, "Dezembro": 5.446},
    },
    "Luciára": {
        "lat": -11.22, "lon": -50.66,
        "global": 5.179,
        "mensal": {"Janeiro": 5.212, "Fevereiro": 5.401, "Março": 5.1, "Abril": 4.96, "Maio": 5.058, "Junho": 5.13, "Julho": 5.349, "Agosto": 5.849, "Setembro": 5.595, "Outubro": 5.408, "Novembro": 5.259, "Dezembro": 5.374},
    },
    "Marcelândia": {
        "lat": -11.04, "lon": -54.64,
        "global": 4.997,
        "mensal": {"Janeiro": 5.11, "Fevereiro": 5.057, "Março": 4.902, "Abril": 4.908, "Maio": 4.88, "Junho": 4.835, "Julho": 5.277, "Agosto": 5.693, "Setembro": 5.263, "Outubro": 5.255, "Novembro": 5.145, "Dezembro": 5.133},
    },
    "Matupá": {
        "lat": -10.12, "lon": -54.93,
        "global": 4.91,
        "mensal": {"Janeiro": 5.013, "Fevereiro": 4.963, "Março": 4.836, "Abril": 4.761, "Maio": 4.845, "Junho": 4.734, "Julho": 5.005, "Agosto": 5.532, "Setembro": 5.179, "Outubro": 5.319, "Novembro": 5.109, "Dezembro": 5.091},
    },
    "Mirassol d'Oeste": {
        "lat": -15.68, "lon": -58.09,
        "global": 4.945,
        "mensal": {"Janeiro": 5.551, "Fevereiro": 5.347, "Março": 5.138, "Abril": 4.869, "Maio": 4.233, "Junho": 4.302, "Julho": 4.409, "Agosto": 5.178, "Setembro": 5.169, "Outubro": 5.372, "Novembro": 5.561, "Dezembro": 5.686},
    },
    "Nobres": {
        "lat": -14.72, "lon": -56.33,
        "global": 5.071,
        "mensal": {"Janeiro": 5.336, "Fevereiro": 5.322, "Março": 5.171, "Abril": 4.966, "Maio": 4.619, "Junho": 4.603, "Julho": 4.825, "Agosto": 5.606, "Setembro": 5.304, "Outubro": 5.368, "Novembro": 5.584, "Dezembro": 5.672},
    },
    "Nortelândia": {
        "lat": -14.46, "lon": -56.79,
        "global": 5.035,
        "mensal": {"Janeiro": 5.406, "Fevereiro": 5.295, "Março": 5.062, "Abril": 4.952, "Maio": 4.599, "Junho": 4.591, "Julho": 4.788, "Agosto": 5.513, "Setembro": 5.252, "Outubro": 5.377, "Novembro": 5.51, "Dezembro": 5.584},
    },
    "Nossa Senhora do Livramento": {
        "lat": -15.77, "lon": -56.34,
        "global": 5.101,
        "mensal": {"Janeiro": 5.62, "Fevereiro": 5.545, "Março": 5.3, "Abril": 5.049, "Maio": 4.488, "Junho": 4.465, "Julho": 4.62, "Agosto": 5.507, "Setembro": 5.224, "Outubro": 5.364, "Novembro": 5.709, "Dezembro": 5.858},
    },
    "Nova Bandeirantes": {
        "lat": -9.84, "lon": -57.76,
        "global": 4.727,
        "mensal": {"Janeiro": 4.675, "Fevereiro": 4.667, "Março": 4.608, "Abril": 4.541, "Maio": 4.504, "Junho": 4.709, "Julho": 4.874, "Agosto": 5.4, "Setembro": 5.052, "Outubro": 5.219, "Novembro": 4.963, "Dezembro": 4.927},
    },
    "Nova Brasilândia": {
        "lat": -14.96, "lon": -54.71,
        "global": 5.12,
        "mensal": {"Janeiro": 5.412, "Fevereiro": 5.323, "Março": 5.14, "Abril": 5.122, "Maio": 4.857, "Junho": 4.797, "Julho": 4.959, "Agosto": 5.736, "Setembro": 5.361, "Outubro": 5.299, "Novembro": 5.458, "Dezembro": 5.515},
    },
    "Nova Canaã do Norte": {
        "lat": -10.56, "lon": -55.27,
        "global": 4.984,
        "mensal": {"Janeiro": 5.164, "Fevereiro": 5.058, "Março": 4.936, "Abril": 4.856, "Maio": 4.831, "Junho": 4.796, "Julho": 5.104, "Agosto": 5.576, "Setembro": 5.283, "Outubro": 5.311, "Novembro": 5.197, "Dezembro": 5.191},
    },
    "Nova Guarita": {
        "lat": -10.22, "lon": -54.66,
        "global": 4.974,
        "mensal": {"Janeiro": 4.979, "Fevereiro": 4.95, "Março": 4.828, "Abril": 4.755, "Maio": 4.858, "Junho": 4.969, "Julho": 5.259, "Agosto": 5.739, "Setembro": 5.277, "Outubro": 5.308, "Novembro": 5.155, "Dezembro": 5.108},
    },
    "Nova Lacerda": {
        "lat": -14.47, "lon": -59.56,
        "global": 4.885,
        "mensal": {"Janeiro": 5.132, "Fevereiro": 4.94, "Março": 4.853, "Abril": 4.792, "Maio": 4.386, "Junho": 4.448, "Julho": 4.655, "Agosto": 5.226, "Setembro": 5.157, "Outubro": 5.399, "Novembro": 5.564, "Dezembro": 5.534},
    },
    "Nova Marilândia": {
        "lat": -14.35, "lon": -56.96,
        "global": 5.001,
        "mensal": {"Janeiro": 5.297, "Fevereiro": 5.221, "Março": 5.037, "Abril": 4.946, "Maio": 4.585, "Junho": 4.583, "Julho": 4.784, "Agosto": 5.57, "Setembro": 5.226, "Outubro": 5.33, "Novembro": 5.423, "Dezembro": 5.508},
    },
    "Nova Maringá": {
        "lat": -13.01, "lon": -57.09,
        "global": 5.018,
        "mensal": {"Janeiro": 5.261, "Fevereiro": 5.127, "Março": 5.041, "Abril": 4.971, "Maio": 4.751, "Junho": 4.738, "Julho": 4.906, "Agosto": 5.387, "Setembro": 5.314, "Outubro": 5.466, "Novembro": 5.328, "Dezembro": 5.423},
    },
    "Nova Monte Verde": {
        "lat": -9.97, "lon": -57.0,
        "global": 4.798,
        "mensal": {"Janeiro": 4.788, "Fevereiro": 4.79, "Março": 4.673, "Abril": 4.609, "Maio": 4.581, "Junho": 4.723, "Julho": 4.878, "Agosto": 5.418, "Setembro": 5.166, "Outubro": 5.313, "Novembro": 5.092, "Dezembro": 4.988},
    },
    "Nova Mutum": {
        "lat": -13.83, "lon": -56.08,
        "global": 5.6,
        "mensal": {"Janeiro": 5.337, "Fevereiro": 5.216, "Março": 5.044, "Abril": 4.978, "Maio": 4.706, "Junho": 4.654, "Julho": 4.902, "Agosto": 5.465, "Setembro": 5.306, "Outubro": 5.408, "Novembro": 5.423, "Dezembro": 5.539},
    },
    "Nova Nazaré": {
        "lat": -14.56, "lon": -51.8,
        "global": 5.32,
        "mensal": {"Janeiro": 5.623, "Fevereiro": 5.801, "Março": 5.429, "Abril": 5.478, "Maio": 5.092, "Junho": 4.817, "Julho": 5.108, "Agosto": 5.682, "Setembro": 5.622, "Outubro": 5.665, "Novembro": 5.499, "Dezembro": 5.63},
    },
    "Nova Olímpia": {
        "lat": -14.8, "lon": -57.29,
        "global": 4.967,
        "mensal": {"Janeiro": 5.35, "Fevereiro": 5.272, "Março": 5.101, "Abril": 4.906, "Maio": 4.449, "Junho": 4.466, "Julho": 4.618, "Agosto": 5.326, "Setembro": 5.124, "Outubro": 5.354, "Novembro": 5.543, "Dezembro": 5.584},
    },
    "Nova Santa Helena": {
        "lat": -10.85, "lon": -54.88,
        "global": 4.955,
        "mensal": {"Janeiro": 5.086, "Fevereiro": 5.017, "Março": 4.9, "Abril": 4.819, "Maio": 4.844, "Junho": 4.783, "Julho": 5.147, "Agosto": 5.605, "Setembro": 5.223, "Outubro": 5.228, "Novembro": 5.186, "Dezembro": 5.106},
    },
    "Nova Ubiratã": {
        "lat": -13.53, "lon": -55.25,
        "global": 5.104,
        "mensal": {"Janeiro": 5.313, "Fevereiro": 5.293, "Março": 5.101, "Abril": 5.096, "Maio": 4.892, "Junho": 4.821, "Julho": 5.109, "Agosto": 5.659, "Setembro": 5.273, "Outubro": 5.382, "Novembro": 5.363, "Dezembro": 5.479},
    },
    "Nova Xavantina": {
        "lat": -14.69, "lon": -52.35,
        "global": 5.306,
        "mensal": {"Janeiro": 5.622, "Fevereiro": 5.774, "Março": 5.459, "Abril": 5.442, "Maio": 5.079, "Junho": 4.758, "Julho": 5.027, "Agosto": 5.626, "Setembro": 5.615, "Outubro": 5.664, "Novembro": 5.558, "Dezembro": 5.647},
    },
    "Novo Horizonte do Norte": {
        "lat": -11.42, "lon": -57.34,
        "global": 4.882,
        "mensal": {"Janeiro": 5.04, "Fevereiro": 4.91, "Março": 4.819, "Abril": 4.741, "Maio": 4.638, "Junho": 4.73, "Julho": 5.001, "Agosto": 5.339, "Setembro": 5.184, "Outubro": 5.35, "Novembro": 5.135, "Dezembro": 5.164},
    },
    "Novo Mundo": {
        "lat": -9.97, "lon": -54.97,
        "global": 4.879,
        "mensal": {"Janeiro": 4.905, "Fevereiro": 4.854, "Março": 4.827, "Abril": 4.729, "Maio": 4.78, "Junho": 4.83, "Julho": 5.029, "Agosto": 5.579, "Setembro": 5.142, "Outubro": 5.248, "Novembro": 5.048, "Dezembro": 5.041},
    },
    "Novo Santo Antônio": {
        "lat": -14.94, "lon": -51.75,
        "global": 5.325,
        "mensal": {"Janeiro": 5.641, "Fevereiro": 5.809, "Março": 5.473, "Abril": 5.456, "Maio": 5.096, "Junho": 4.803, "Julho": 5.104, "Agosto": 5.723, "Setembro": 5.6, "Outubro": 5.67, "Novembro": 5.496, "Dezembro": 5.626},
    },
    "Novo São Joaquim": {
        "lat": -14.68, "lon": -53.05,
        "global": 5.293,
        "mensal": {"Janeiro": 5.565, "Fevereiro": 5.676, "Março": 5.387, "Abril": 5.52, "Maio": 5.099, "Junho": 4.884, "Julho": 5.166, "Agosto": 5.691, "Setembro": 5.481, "Outubro": 5.574, "Novembro": 5.446, "Dezembro": 5.609},
    },
    "Paranatinga": {
        "lat": -14.43, "lon": -54.05,
        "global": 5.18,
        "mensal": {"Janeiro": 5.439, "Fevereiro": 5.481, "Março": 5.214, "Abril": 5.316, "Maio": 4.934, "Junho": 4.818, "Julho": 5.03, "Agosto": 5.669, "Setembro": 5.378, "Outubro": 5.496, "Novembro": 5.422, "Dezembro": 5.514},
    },
    "Paranaíta": {
        "lat": -9.67, "lon": -56.48,
        "global": 4.798,
        "mensal": {"Janeiro": 4.817, "Fevereiro": 4.814, "Março": 4.69, "Abril": 4.558, "Maio": 4.599, "Junho": 4.763, "Julho": 4.888, "Agosto": 5.409, "Setembro": 5.177, "Outubro": 5.259, "Novembro": 5.037, "Dezembro": 5.0},
    },
    "Pedra Preta": {
        "lat": -16.62, "lon": -54.47,
        "global": 5.253,
        "mensal": {"Janeiro": 5.782, "Fevereiro": 5.778, "Março": 5.517, "Abril": 5.284, "Maio": 4.792, "Junho": 4.583, "Julho": 4.722, "Agosto": 5.595, "Setembro": 5.366, "Outubro": 5.501, "Novembro": 5.797, "Dezembro": 5.902},
    },
    "Peixoto de Azevedo": {
        "lat": -10.23, "lon": -54.99,
        "global": 5.36,
        "mensal": {"Janeiro": 5.067, "Fevereiro": 5.031, "Março": 4.891, "Abril": 4.809, "Maio": 4.838, "Junho": 4.705, "Julho": 5.005, "Agosto": 5.539, "Setembro": 5.241, "Outubro": 5.386, "Novembro": 5.17, "Dezembro": 5.159},
    },
    "Planalto da Serra": {
        "lat": -14.65, "lon": -54.79,
        "global": 5.171,
        "mensal": {"Janeiro": 5.437, "Fevereiro": 5.414, "Março": 5.276, "Abril": 5.311, "Maio": 4.927, "Junho": 4.786, "Julho": 4.956, "Agosto": 5.697, "Setembro": 5.374, "Outubro": 5.43, "Novembro": 5.485, "Dezembro": 5.51},
    },
    "Poconé": {
        "lat": -16.26, "lon": -56.62,
        "global": 5.56,
        "mensal": {"Janeiro": 5.675, "Fevereiro": 5.567, "Março": 5.288, "Abril": 4.982, "Maio": 4.366, "Junho": 4.315, "Julho": 4.484, "Agosto": 5.374, "Setembro": 5.173, "Outubro": 5.464, "Novembro": 5.667, "Dezembro": 5.942},
    },
    "Pontal da Araguaia": {
        "lat": -15.9, "lon": -52.02,
        "global": 5.277,
        "mensal": {"Janeiro": 5.646, "Fevereiro": 5.848, "Março": 5.432, "Abril": 5.471, "Maio": 5.06, "Junho": 4.652, "Julho": 4.86, "Agosto": 5.537, "Setembro": 5.448, "Outubro": 5.657, "Novembro": 5.554, "Dezembro": 5.744},
    },
    "Ponte Branca": {
        "lat": -16.73, "lon": -52.68,
        "global": 5.261,
        "mensal": {"Janeiro": 5.706, "Fevereiro": 5.811, "Março": 5.403, "Abril": 5.347, "Maio": 4.939, "Junho": 4.631, "Julho": 4.71, "Agosto": 5.588, "Setembro": 5.514, "Outubro": 5.49, "Novembro": 5.693, "Dezembro": 5.878},
    },
    "Pontes e Lacerda": {
        "lat": -15.23, "lon": -59.33,
        "global": 5.48,
        "mensal": {"Janeiro": 5.341, "Fevereiro": 5.144, "Março": 4.984, "Abril": 4.902, "Maio": 4.317, "Junho": 4.392, "Julho": 4.523, "Agosto": 5.152, "Setembro": 5.209, "Outubro": 5.467, "Novembro": 5.679, "Dezembro": 5.623},
    },
    "Porto Alegre do Norte": {
        "lat": -10.87, "lon": -51.65,
        "global": 5.069,
        "mensal": {"Janeiro": 5.135, "Fevereiro": 5.275, "Março": 5.048, "Abril": 4.867, "Maio": 5.019, "Junho": 4.842, "Julho": 5.145, "Agosto": 5.701, "Setembro": 5.406, "Outubro": 5.344, "Novembro": 5.25, "Dezembro": 5.324},
    },
    "Porto Esperidião": {
        "lat": -15.85, "lon": -58.46,
        "global": 4.969,
        "mensal": {"Janeiro": 5.588, "Fevereiro": 5.43, "Março": 5.16, "Abril": 4.888, "Maio": 4.164, "Junho": 4.222, "Julho": 4.376, "Agosto": 5.098, "Setembro": 5.205, "Outubro": 5.494, "Novembro": 5.701, "Dezembro": 5.787},
    },
    "Porto Estrela": {
        "lat": -15.31, "lon": -57.22,
        "global": 5.064,
        "mensal": {"Janeiro": 5.533, "Fevereiro": 5.412, "Março": 5.262, "Abril": 4.984, "Maio": 4.515, "Junho": 4.501, "Julho": 4.634, "Agosto": 5.255, "Setembro": 5.266, "Outubro": 5.469, "Novembro": 5.684, "Dezembro": 5.775},
    },
    "Porto dos Gaúchos": {
        "lat": -11.53, "lon": -57.41,
        "global": 4.879,
        "mensal": {"Janeiro": 5.02, "Fevereiro": 4.886, "Março": 4.81, "Abril": 4.771, "Maio": 4.66, "Junho": 4.761, "Julho": 4.967, "Agosto": 5.351, "Setembro": 5.176, "Outubro": 5.327, "Novembro": 5.111, "Dezembro": 5.171},
    },
    "Poxoréo": {
        "lat": -15.83, "lon": -54.38,
        "global": 5.134,
        "mensal": {"Janeiro": 5.459, "Fevereiro": 5.446, "Março": 5.246, "Abril": 5.198, "Maio": 4.825, "Junho": 4.688, "Julho": 4.858, "Agosto": 5.785, "Setembro": 5.304, "Outubro": 5.299, "Novembro": 5.537, "Dezembro": 5.496},
    },
    "Primavera do Leste": {
        "lat": -15.56, "lon": -54.3,
        "global": 5.53,
        "mensal": {"Janeiro": 5.541, "Fevereiro": 5.424, "Março": 5.144, "Abril": 5.181, "Maio": 4.861, "Junho": 4.664, "Julho": 4.839, "Agosto": 5.652, "Setembro": 5.293, "Outubro": 5.27, "Novembro": 5.428, "Dezembro": 5.557},
    },
    "Querência": {
        "lat": -12.61, "lon": -52.19,
        "global": 5.144,
        "mensal": {"Janeiro": 5.314, "Fevereiro": 5.496, "Março": 5.077, "Abril": 5.098, "Maio": 5.047, "Junho": 4.857, "Julho": 5.285, "Agosto": 5.613, "Setembro": 5.434, "Outubro": 5.42, "Novembro": 5.249, "Dezembro": 5.376},
    },
    "Reserva do Cabaçal": {
        "lat": -15.06, "lon": -58.48,
        "global": 4.707,
        "mensal": {"Janeiro": 4.995, "Fevereiro": 4.859, "Março": 4.709, "Abril": 4.603, "Maio": 4.144, "Junho": 4.331, "Julho": 4.494, "Agosto": 5.326, "Setembro": 4.981, "Outubro": 5.051, "Novembro": 5.217, "Dezembro": 5.189},
    },
    "Ribeirão Cascalheira": {
        "lat": -12.94, "lon": -51.82,
        "global": 5.208,
        "mensal": {"Janeiro": 5.29, "Fevereiro": 5.436, "Março": 5.192, "Abril": 5.205, "Maio": 5.098, "Junho": 4.969, "Julho": 5.368, "Agosto": 5.843, "Setembro": 5.548, "Outubro": 5.424, "Novembro": 5.276, "Dezembro": 5.402},
    },
    "Ribeirãozinho": {
        "lat": -16.47, "lon": -52.67,
        "global": 5.258,
        "mensal": {"Janeiro": 5.745, "Fevereiro": 5.8, "Março": 5.374, "Abril": 5.37, "Maio": 4.942, "Junho": 4.625, "Julho": 4.671, "Agosto": 5.516, "Setembro": 5.517, "Outubro": 5.523, "Novembro": 5.731, "Dezembro": 5.853},
    },
    "Rio Branco": {
        "lat": -15.25, "lon": -58.1,
        "global": 4.829,
        "mensal": {"Janeiro": 5.19, "Fevereiro": 5.088, "Março": 4.929, "Abril": 4.792, "Maio": 4.267, "Junho": 4.375, "Julho": 4.484, "Agosto": 5.299, "Setembro": 5.085, "Outubro": 5.177, "Novembro": 5.393, "Dezembro": 5.32},
    },
    "Rondolândia": {
        "lat": -10.79, "lon": -61.45,
        "global": 4.594,
        "mensal": {"Janeiro": 4.511, "Fevereiro": 4.367, "Março": 4.492, "Abril": 4.53, "Maio": 4.165, "Junho": 4.6, "Julho": 4.736, "Agosto": 5.148, "Setembro": 5.074, "Outubro": 5.227, "Novembro": 4.933, "Dezembro": 4.732},
    },
    "Rondonópolis": {
        "lat": -16.47, "lon": -54.64,
        "global": 5.45,
        "mensal": {"Janeiro": 5.677, "Fevereiro": 5.651, "Março": 5.396, "Abril": 5.195, "Maio": 4.725, "Junho": 4.528, "Julho": 4.674, "Agosto": 5.599, "Setembro": 5.336, "Outubro": 5.408, "Novembro": 5.632, "Dezembro": 5.783},
    },
    "Rosário Oeste": {
        "lat": -14.84, "lon": -56.42,
        "global": 5.072,
        "mensal": {"Janeiro": 5.325, "Fevereiro": 5.367, "Março": 5.19, "Abril": 5.009, "Maio": 4.606, "Junho": 4.586, "Julho": 4.761, "Agosto": 5.562, "Setembro": 5.265, "Outubro": 5.374, "Novembro": 5.642, "Dezembro": 5.707},
    },
    "Salto do Céu": {
        "lat": -15.11, "lon": -58.13,
        "global": 4.793,
        "mensal": {"Janeiro": 5.052, "Fevereiro": 4.98, "Março": 4.851, "Abril": 4.781, "Maio": 4.285, "Junho": 4.4, "Julho": 4.518, "Agosto": 5.312, "Setembro": 5.058, "Outubro": 5.141, "Novembro": 5.346, "Dezembro": 5.231},
    },
    "Santa Carmem": {
        "lat": -11.96, "lon": -55.25,
        "global": 5.037,
        "mensal": {"Janeiro": 5.271, "Fevereiro": 5.154, "Março": 5.064, "Abril": 5.008, "Maio": 4.877, "Junho": 4.742, "Julho": 5.088, "Agosto": 5.407, "Setembro": 5.28, "Outubro": 5.433, "Novembro": 5.267, "Dezembro": 5.361},
    },
    "Santa Cruz do Xingu": {
        "lat": -10.13, "lon": -52.4,
        "global": 4.986,
        "mensal": {"Janeiro": 4.959, "Fevereiro": 5.119, "Março": 4.872, "Abril": 4.712, "Maio": 4.886, "Junho": 4.925, "Julho": 5.161, "Agosto": 5.752, "Setembro": 5.365, "Outubro": 5.275, "Novembro": 5.156, "Dezembro": 5.151},
    },
    "Santa Rita do Trivelato": {
        "lat": -13.86, "lon": -55.33,
        "global": 5.071,
        "mensal": {"Janeiro": 5.344, "Fevereiro": 5.293, "Março": 5.059, "Abril": 5.142, "Maio": 4.863, "Junho": 4.723, "Julho": 4.959, "Agosto": 5.457, "Setembro": 5.285, "Outubro": 5.392, "Novembro": 5.375, "Dezembro": 5.475},
    },
    "Santa Terezinha": {
        "lat": -10.47, "lon": -50.52,
        "global": 5.121,
        "mensal": {"Janeiro": 5.159, "Fevereiro": 5.269, "Março": 5.018, "Abril": 4.885, "Maio": 5.011, "Junho": 5.099, "Julho": 5.386, "Agosto": 5.904, "Setembro": 5.533, "Outubro": 5.285, "Novembro": 5.194, "Dezembro": 5.24},
    },
    "Santo Afonso": {
        "lat": -14.49, "lon": -57.01,
        "global": 5.003,
        "mensal": {"Janeiro": 5.274, "Fevereiro": 5.279, "Março": 5.093, "Abril": 4.95, "Maio": 4.542, "Junho": 4.557, "Julho": 4.729, "Agosto": 5.477, "Setembro": 5.23, "Outubro": 5.363, "Novembro": 5.472, "Dezembro": 5.564},
    },
    "Santo Antônio do Leste": {
        "lat": -14.82, "lon": -54.14,
        "global": 5.151,
        "mensal": {"Janeiro": 5.479, "Fevereiro": 5.507, "Março": 5.212, "Abril": 5.166, "Maio": 4.876, "Junho": 4.796, "Julho": 4.94, "Agosto": 5.617, "Setembro": 5.368, "Outubro": 5.407, "Novembro": 5.382, "Dezembro": 5.61},
    },
    "Santo Antônio do Leverger": {
        "lat": -15.87, "lon": -55.44,
        "global": 4.962,
        "mensal": {"Janeiro": 5.29, "Fevereiro": 5.138, "Março": 4.949, "Abril": 4.848, "Maio": 4.56, "Junho": 4.525, "Julho": 4.721, "Agosto": 5.62, "Setembro": 5.185, "Outubro": 5.206, "Novembro": 5.454, "Dezembro": 5.534},
    },
    "Sapezal": {
        "lat": -13.54, "lon": -58.81,
        "global": 5.48,
        "mensal": {"Janeiro": 5.078, "Fevereiro": 4.9, "Março": 4.906, "Abril": 4.782, "Maio": 4.427, "Junho": 4.469, "Julho": 4.602, "Agosto": 5.178, "Setembro": 5.01, "Outubro": 5.196, "Novembro": 5.339, "Dezembro": 5.393},
    },
    "Serra Nova Dourada": {
        "lat": -12.09, "lon": -51.41,
        "global": 5.169,
        "mensal": {"Janeiro": 5.199, "Fevereiro": 5.326, "Março": 5.099, "Abril": 5.044, "Maio": 5.101, "Junho": 4.992, "Julho": 5.33, "Agosto": 5.923, "Setembro": 5.505, "Outubro": 5.425, "Novembro": 5.291, "Dezembro": 5.343},
    },
    "Sinop": {
        "lat": -11.86, "lon": -55.51,
        "global": 5.51,
        "mensal": {"Janeiro": 5.2, "Fevereiro": 5.091, "Março": 5.053, "Abril": 4.943, "Maio": 4.757, "Junho": 4.716, "Julho": 5.008, "Agosto": 5.334, "Setembro": 5.233, "Outubro": 5.422, "Novembro": 5.197, "Dezembro": 5.34},
    },
    "Sorriso": {
        "lat": -12.55, "lon": -55.71,
        "global": 5.59,
        "mensal": {"Janeiro": 5.335, "Fevereiro": 5.179, "Março": 5.094, "Abril": 5.04, "Maio": 4.843, "Junho": 4.722, "Julho": 4.986, "Agosto": 5.371, "Setembro": 5.229, "Outubro": 5.429, "Novembro": 5.271, "Dezembro": 5.37},
    },
    "São Félix do Araguaia": {
        "lat": -11.61, "lon": -50.67,
        "global": 5.208,
        "mensal": {"Janeiro": 5.265, "Fevereiro": 5.385, "Março": 5.195, "Abril": 5.035, "Maio": 5.084, "Junho": 5.015, "Julho": 5.403, "Agosto": 5.902, "Setembro": 5.62, "Outubro": 5.427, "Novembro": 5.314, "Dezembro": 5.42},
    },
    "São José do Povo": {
        "lat": -16.87, "lon": -54.27,
        "global": 5.252,
        "mensal": {"Janeiro": 5.776, "Fevereiro": 5.771, "Março": 5.495, "Abril": 5.272, "Maio": 4.775, "Junho": 4.526, "Julho": 4.722, "Agosto": 5.584, "Setembro": 5.411, "Outubro": 5.493, "Novembro": 5.846, "Dezembro": 5.936},
    },
    "São José do Rio Claro": {
        "lat": -13.44, "lon": -56.73,
        "global": 5.054,
        "mensal": {"Janeiro": 5.295, "Fevereiro": 5.15, "Março": 5.092, "Abril": 5.009, "Maio": 4.789, "Junho": 4.715, "Julho": 4.897, "Agosto": 5.45, "Setembro": 5.335, "Outubro": 5.561, "Novembro": 5.428, "Dezembro": 5.442},
    },
    "São José do Xingu": {
        "lat": -10.8, "lon": -52.75,
        "global": 5.055,
        "mensal": {"Janeiro": 5.101, "Fevereiro": 5.202, "Março": 4.958, "Abril": 4.889, "Maio": 4.968, "Junho": 4.995, "Julho": 5.277, "Agosto": 5.761, "Setembro": 5.36, "Outubro": 5.201, "Novembro": 5.149, "Dezembro": 5.309},
    },
    "São José dos Quatro Marcos": {
        "lat": -15.63, "lon": -58.19,
        "global": 4.94,
        "mensal": {"Janeiro": 5.526, "Fevereiro": 5.356, "Março": 5.124, "Abril": 4.862, "Maio": 4.214, "Junho": 4.305, "Julho": 4.397, "Agosto": 5.166, "Setembro": 5.179, "Outubro": 5.364, "Novembro": 5.576, "Dezembro": 5.695},
    },
    "São Pedro da Cipa": {
        "lat": -16.27, "lon": -54.73,
        "global": 5.159,
        "mensal": {"Janeiro": 5.642, "Fevereiro": 5.599, "Março": 5.359, "Abril": 5.183, "Maio": 4.755, "Junho": 4.583, "Julho": 4.722, "Agosto": 5.639, "Setembro": 5.27, "Outubro": 5.357, "Novembro": 5.585, "Dezembro": 5.765},
    },
    "Tabaporã": {
        "lat": -11.58, "lon": -57.53,
        "global": 4.867,
        "mensal": {"Janeiro": 4.978, "Fevereiro": 4.89, "Março": 4.815, "Abril": 4.77, "Maio": 4.66, "Junho": 4.742, "Julho": 4.943, "Agosto": 5.357, "Setembro": 5.162, "Outubro": 5.308, "Novembro": 5.08, "Dezembro": 5.156},
    },
    "Tangará da Serra": {
        "lat": -14.62, "lon": -57.5,
        "global": 5.42,
        "mensal": {"Janeiro": 5.234, "Fevereiro": 5.195, "Março": 5.076, "Abril": 4.868, "Maio": 4.442, "Junho": 4.482, "Julho": 4.66, "Agosto": 5.405, "Setembro": 5.173, "Outubro": 5.342, "Novembro": 5.413, "Dezembro": 5.539},
    },
    "Tapurah": {
        "lat": -12.68, "lon": -56.51,
        "global": 5.019,
        "mensal": {"Janeiro": 5.238, "Fevereiro": 5.111, "Março": 5.038, "Abril": 4.939, "Maio": 4.785, "Junho": 4.769, "Julho": 4.971, "Agosto": 5.402, "Setembro": 5.293, "Outubro": 5.497, "Novembro": 5.301, "Dezembro": 5.384},
    },
    "Terra Nova do Norte": {
        "lat": -10.52, "lon": -55.22,
        "global": 4.991,
        "mensal": {"Janeiro": 5.151, "Fevereiro": 5.067, "Março": 4.948, "Abril": 4.841, "Maio": 4.836, "Junho": 4.804, "Julho": 5.125, "Agosto": 5.607, "Setembro": 5.293, "Outubro": 5.323, "Novembro": 5.198, "Dezembro": 5.197},
    },
    "Tesouro": {
        "lat": -16.08, "lon": -53.56,
        "global": 5.244,
        "mensal": {"Janeiro": 5.66, "Fevereiro": 5.658, "Março": 5.32, "Abril": 5.361, "Maio": 4.95, "Junho": 4.696, "Julho": 4.866, "Agosto": 5.675, "Setembro": 5.532, "Outubro": 5.488, "Novembro": 5.616, "Dezembro": 5.684},
    },
    "Torixoréu": {
        "lat": -16.2, "lon": -52.56,
        "global": 5.275,
        "mensal": {"Janeiro": 5.66, "Fevereiro": 5.774, "Março": 5.38, "Abril": 5.451, "Maio": 5.003, "Junho": 4.662, "Julho": 4.786, "Agosto": 5.573, "Setembro": 5.559, "Outubro": 5.597, "Novembro": 5.671, "Dezembro": 5.769},
    },
    "União do Sul": {
        "lat": -11.48, "lon": -54.31,
        "global": 5.06,
        "mensal": {"Janeiro": 5.163, "Fevereiro": 5.198, "Março": 4.97, "Abril": 5.022, "Maio": 4.978, "Junho": 4.912, "Julho": 5.28, "Agosto": 5.668, "Setembro": 5.304, "Outubro": 5.304, "Novembro": 5.188, "Dezembro": 5.245},
    },
    "Vale de São Domingos": {
        "lat": -15.11, "lon": -59.02,
        "global": 4.82,
        "mensal": {"Janeiro": 5.168, "Fevereiro": 4.938, "Março": 4.81, "Abril": 4.658, "Maio": 4.208, "Junho": 4.376, "Julho": 4.492, "Agosto": 5.214, "Setembro": 5.098, "Outubro": 5.296, "Novembro": 5.514, "Dezembro": 5.508},
    },
    "Vera": {
        "lat": -12.3, "lon": -55.31,
        "global": 5.036,
        "mensal": {"Janeiro": 5.231, "Fevereiro": 5.181, "Março": 5.064, "Abril": 5.023, "Maio": 4.86, "Junho": 4.801, "Julho": 5.063, "Agosto": 5.363, "Setembro": 5.237, "Outubro": 5.388, "Novembro": 5.29, "Dezembro": 5.448},
    },
    "Vila Bela da Santíssima Trindade": {
        "lat": -14.98, "lon": -59.94,
        "global": 4.891,
        "mensal": {"Janeiro": 5.245, "Fevereiro": 5.033, "Março": 5.015, "Abril": 4.893, "Maio": 4.293, "Junho": 4.395, "Julho": 4.551, "Agosto": 5.226, "Setembro": 5.158, "Outubro": 5.406, "Novembro": 5.523, "Dezembro": 5.421},
    },
    "Vila Rica": {
        "lat": -9.98, "lon": -51.12,
        "global": 5.04,
        "mensal": {"Janeiro": 5.076, "Fevereiro": 5.104, "Março": 4.935, "Abril": 4.864, "Maio": 4.888, "Junho": 5.039, "Julho": 5.266, "Agosto": 5.824, "Setembro": 5.415, "Outubro": 5.213, "Novembro": 5.122, "Dezembro": 5.249},
    },
    "Várzea Grande": {
        "lat": -15.65, "lon": -56.13,
        "global": 5.58,
        "mensal": {"Janeiro": 5.638, "Fevereiro": 5.495, "Março": 5.323, "Abril": 5.065, "Maio": 4.544, "Junho": 4.479, "Julho": 4.64, "Agosto": 5.552, "Setembro": 5.253, "Outubro": 5.446, "Novembro": 5.726, "Dezembro": 5.915},
    },
    "Água Boa": {
        "lat": -14.02, "lon": -52.16,
        "global": 5.254,
        "mensal": {"Janeiro": 5.385, "Fevereiro": 5.668, "Março": 5.309, "Abril": 5.346, "Maio": 5.099, "Junho": 4.828, "Julho": 5.194, "Agosto": 5.669, "Setembro": 5.562, "Outubro": 5.576, "Novembro": 5.433, "Dezembro": 5.547},
    },
}

# Fallback: média MT — Atlas Fig.65 (Centro-Oeste: 5,07 kWh/m²/dia GHI)
FALLBACK_MT = {
    "lat": -12.64, "lon": -55.49, "global": 5.48,
    "mensal": {"Janeiro":5.31,"Fevereiro":5.34,"Março":5.20,"Abril":5.25,
               "Maio":5.12,"Junho":5.05,"Julho":5.18,"Agosto":5.55,
               "Setembro":5.38,"Outubro":5.42,"Novembro":5.28,"Dezembro":5.22},
}

def buscar_dados_municipio(nome: str) -> dict:
    """Retorna dados solares ou fallback estadual se município não encontrado."""
    return DADOS_SOLAR_MT.get(nome.strip(), FALLBACK_MT)

MUNICIPIOS = sorted(DADOS_SOLAR_MT.keys())