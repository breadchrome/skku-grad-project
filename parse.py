if __name__ == "__main__":
    deviceObjects = WiFiDeviceFactory()
    print(deviceObjects)

    intel = deviceObjects.CreateDevice('intel')
    test = CSIExtractor(intel)

    test.OpenCSIFile('../csi.dat')
    csi = test.GetCSI()
    elem = csi[28]['csi']
    test.ConvertToCSIMatrix()

    print('receiver:', test.ReceiverAntennaCount(), ' Transmitter:', test.TransmitterAntennaCount())

    # convert to numpy matrix data structure to be used in all processing
    temp = np.zeros((3,3,30,2500), complex)
    for y in range(3): # transmitter
        for x in range(3): # receiver
            temp[y,x,:,0] = elem[:,y,x]

    temp = temp[..., np.newaxis]
    #print(temp.shape)
    new = np.zeros((3,3,30), complex)

    #print(temp[:,:,:,0])
    #print(elem[:,0,0])

    #print(np.reshape(elem, (1,3,30)))

    # Atheros test is here
    # test = CSIExtractor(deviceObjects.CreateDevice('atheros'))
    # plot = CSI_Plot()

    #Continous wavelet transform
    from scipy import signal
    import matplotlib.pyplot as plt
    t = np.linspace(-1, 1, 200, endpoint=False)
    sig  = np.cos(2 * np.pi * 7 * t) + signal.gausspulse(t - 0.4, fc=2)
    print(sig.shape)
    widths = np.arange(6, 9)
    cwtmatr = signal.cwt(sig, signal.ricker, widths)
    print(cwtmatr.shape)
    plt.imshow(cwtmatr, extent=[-1, 1, 31, 1], cmap='PRGn', aspect='auto',
            vmax=abs(cwtmatr).max(), vmin=-abs(cwtmatr).max())
    plt.show()
