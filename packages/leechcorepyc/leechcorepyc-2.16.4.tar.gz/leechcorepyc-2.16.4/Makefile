
all:
	$(MAKE) -C leechcore
	$(MAKE) -C leechcore_ft601_driver_linux || true
	$(MAKE) -C leechcore_device_qemu || true
	$(MAKE) -C leechcore_device_rawtcp || true
	cp files/leechcore.so .
	cp files/*.so leechcorepyc/

clean:
	$(MAKE) clean -C leechcore
	$(MAKE) clean -C leechcore_ft601_driver_linux || true
	$(MAKE) clean -C leechcore_device_qemu || true
	$(MAKE) clean -C leechcore_device_rawtcp || true
	rm files/*.so || true
	rm leechcore.so || true
	rm leechcorepyc/*.so || true

