def count_trains_by_year(data, year):
    year_data = data[data["year"] == year]
    # Calculer la somme des trains programmés pour l'année
    return year_data["Number of scheduled trains"].sum()


def count_delays_by_year(data, year):
    year_data = data[data["year"] == year]
    # Calculer la somme des trains programmés pour l'année
    return year_data["Number of trains delayed at departure"].sum()


def count_cancellations_by_year(data, year):
    # Filtrer les données pour l'année spécifiée
    year_data = data[data["year"] == year]
    return year_data["Number of cancelled trains"].sum()


def get_mean_delayed(data, year):
    year_data = data[data["year"] == year]
    buffer = 0
    count = 0
    for row in year_data["Average delay of late trains at departure"]:
        buffer += row
        count += 1
    if count == 0:
        return round(buffer, 2)
    return round(buffer / count, 2)


# tu voulais faire le on_time_rate mais les datas sont pas ouf

# def get_on_time_rate(data, year):
#     year_data = data[data['year'] == year]
#     tt_trains = year_data['Number of scheduled trains'].sum()
#     nb_delayed = year_data['Number of trains delayed at departure'].sum()
#     nb_cancelled = year_data['Number of cancelled trains'].sum()

#     count_on_time = tt_trains - (nb_cancelled + nb_delayed)
#     count_on_time = round((count_on_time * 100) / tt_trains, 2)
#     return f"{count_on_time}%"
