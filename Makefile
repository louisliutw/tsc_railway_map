YEAR=1978

OUTPUT=tsc_railway_map.kml
.PHONY: clean all


all: $(OUTPUT)


$(OUTPUT): $(YEAR)/*.geojson tokml.py
	./tokml.py $(YEAR)

clean:
	rm -f $(OUTPUT)
