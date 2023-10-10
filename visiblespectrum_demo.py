import visiblespectrum


def main():

    print("--------------------")
    print("| codedrome.com    |")
    print("| Visible Spectrum |")
    print("--------------------\n")

    data = visiblespectrum.generate_data()

    visiblespectrum.print_data(data)

    visiblespectrum.plot_wavelength_frequency(data, "wavelength_frequency.png")

    visiblespectrum.plot_frequency_wavelength(data, "frequency_wavelength.png")


main()
