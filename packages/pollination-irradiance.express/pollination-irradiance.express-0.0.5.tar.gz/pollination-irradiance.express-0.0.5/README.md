# Irradiance Express

Irradiance Express recipe for Pollination

This recipe calculate the solar irradiance (W/m2) for each timestep provided in the wea
file. Nigh-time hours are filtered before running the simulation. To match the results
for each hours see the list of hours in sun-up-hours.txt.

# Limitations

This recipe uses Radiance's `gendaymtx` to generate the sky. "Gendaymtx takes a weather
tape as input and produces a matrix of sky patch values using the Perez all weather
model". "If there is a sun in the description, gendaymtx will include its contribution
in the four nearest sky patches, distributing energy according to centroid proximity".
This means that the value of direct sun is diffused between these patches. This
approximation is fine for studies such as cumulative radiation or for outdoor studies
where the amount of exact direct radiation is not critical. For accurate accounting
of direct sun see the [Irradiance](https://github.com/pollination/irradiance) recipe.
