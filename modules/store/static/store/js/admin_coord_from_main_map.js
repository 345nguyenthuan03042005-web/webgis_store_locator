(function () {
  function byId(id) {
    return document.getElementById(id);
  }

  function ensureSourceInput(formEl) {
    let sourceInput = byId("id_coord_from_map");
    if (sourceInput) return sourceInput;
    sourceInput = document.createElement("input");
    sourceInput.type = "hidden";
    sourceInput.name = "_coord_from_map";
    sourceInput.id = "id_coord_from_map";
    sourceInput.value = "";
    formEl.appendChild(sourceInput);
    return sourceInput;
  }

  function setSource(source) {
    const latInput = byId("id_vi_do");
    if (!latInput) return;
    const formEl = latInput.closest("form");
    if (!formEl) return;

    const sourceInput = ensureSourceInput(formEl);
    sourceInput.value = source;

    const status = byId("coord-source-status");
    if (!status) return;
    if (source === "map") {
      status.textContent = "Ngu\u1ed3n t\u1ecda \u0111\u1ed9: b\u1ea3n \u0111\u1ed3 (\u0111\u1ed9 ch\u00ednh x\u00e1c cao).";
    } else if (source === "address_pending") {
      status.textContent = "\u0110\u00e3 t\u00ecm \u0111\u01b0\u1ee3c v\u1ecb tr\u00ed g\u1ea7n \u0111\u00fang t\u1eeb \u0111\u1ecba ch\u1ec9. T\u1ecda \u0111\u1ed9 hi\u1ec7n t\u1ea1i ch\u01b0a \u0111\u1ed5i; b\u1ea1n ph\u1ea3i click tr\u00ean b\u1ea3n \u0111\u1ed3 \u0111\u1ec3 ch\u1ed1t.";
    } else {
      status.textContent = "";
    }
  }

  function setAddressPending(lat, lon) {
    setSource("address_pending");
    const status = byId("coord-source-status");
    if (status && Number.isFinite(lat) && Number.isFinite(lon)) {
      status.textContent =
        "\u0110\u00e3 t\u00ecm \u0111\u01b0\u1ee3c v\u1ecb tr\u00ed g\u1ea7n \u0111\u00fang: " +
        Number(lat).toFixed(6) +
        ", " +
        Number(lon).toFixed(6) +
        ". T\u1ecda \u0111\u1ed9 hi\u1ec7n t\u1ea1i ch\u01b0a \u0111\u1ed5i; b\u1ea1n ph\u1ea3i click tr\u00ean b\u1ea3n \u0111\u1ed3 \u0111\u1ec3 ch\u1ed1t.";
    }
  }

  function openPickMap(centerLat, centerLon) {
    const url = new URL("/", window.location.origin);
    url.searchParams.set("pick_for", "admin_cuahang");
    if (Number.isFinite(centerLat) && Number.isFinite(centerLon)) {
      url.searchParams.set("center_lat", String(centerLat));
      url.searchParams.set("center_lon", String(centerLon));
    }

    const popup = window.open(url.toString(), "pickCoord", "width=1280,height=860");
    if (!popup) {
      if (
        window.confirm(
          "Tr\u00ecnh duy\u1ec7t \u0111ang ch\u1eb7n popup map. B\u1ea5m OK \u0111\u1ec3 m\u1edf map trong c\u00f9ng tab."
        )
      ) {
        window.location.href = url.toString();
      }
    }
  }

  function setCoords(lat, lon, source) {
    const latInput = byId("id_vi_do");
    const lonInput = byId("id_kinh_do");
    if (!latInput || !lonInput) return;
    latInput.value = Number(lat).toFixed(13);
    lonInput.value = Number(lon).toFixed(13);
    setSource(source || "map");
  }

  async function geocodeAddress(query) {
    const url = "/tools/geocode/?q=" + encodeURIComponent(query);
    const res = await fetch(url, {
      headers: { Accept: "application/json" },
    });
    if (!res.ok) throw new Error("geocode_failed");
    const payload = await res.json();
    const location = payload && payload.location ? payload.location : null;
    if (!location) return null;
    return {
      lat: Number.parseFloat(location.lat),
      lon: Number.parseFloat(location.lon),
    };
  }

  function buildPickUi() {
    const latInput = byId("id_vi_do");
    const lonInput = byId("id_kinh_do");
    if (!latInput || !lonInput) return;

    [latInput, lonInput].forEach(function (input) {
      input.readOnly = true;
      input.title = "Kh\u00f4ng \u0111\u01b0\u1ee3c nh\u1eadp tr\u1ef1c ti\u1ebfp. H\u00e3y l\u1ea5y t\u1eeb \u0111\u1ecba ch\u1ec9 ho\u1eb7c b\u1ea3n \u0111\u1ed3.";
    });

    const mapBtn = byId("btn-pick-coord-main-map");
    if (mapBtn) {
      mapBtn.addEventListener("click", function () {
        const lat = Number.parseFloat(latInput.value);
        const lon = Number.parseFloat(lonInput.value);
        openPickMap(lat, lon);
      });
    }

    const geocodeBtn = byId("btn-geocode-address-admin");
    if (geocodeBtn) {
      geocodeBtn.addEventListener("click", async function () {
        const addressInput = byId("id_dia_chi");
        const query = (addressInput && addressInput.value ? addressInput.value : "").trim();
        if (!query) {
          window.alert("Vui l\u00f2ng nh\u1eadp \u0111\u1ecba ch\u1ec9 tr\u01b0\u1edbc.");
          return;
        }
        geocodeBtn.disabled = true;
        try {
          const found = await geocodeAddress(query);
          if (!found || !Number.isFinite(found.lat) || !Number.isFinite(found.lon)) {
            window.alert("Kh\u00f4ng t\u00ecm th\u1ea5y t\u1ecda \u0111\u1ed9 t\u1eeb \u0111\u1ecba ch\u1ec9. Th\u1eed r\u00fat g\u1ecdn \u0111\u1ecba ch\u1ec9 (b\u1ecf t\u00ean t\u00f2a nh\u00e0/cao \u1ed1c) r\u1ed3i th\u1eed l\u1ea1i.");
            return;
          }
          // Do not overwrite saved coordinates with approximate geocode.
          // Geocode is only used to center the map for manual confirmation.
          setAddressPending(found.lat, found.lon);
          openPickMap(found.lat, found.lon);
        } catch (_e) {
          window.alert("Kh\u00f4ng th\u1ec3 l\u1ea5y t\u1ecda \u0111\u1ed9 t\u1eeb \u0111\u1ecba ch\u1ec9 l\u00fac n\u00e0y.");
        } finally {
          geocodeBtn.disabled = false;
        }
      });
    }
  }

  function tryReadLocalStorageFallback() {
    try {
      const raw = localStorage.getItem("admin_coord_pick");
      if (!raw) return;
      const data = JSON.parse(raw);
      if (!data || data.type !== "admin_coord_pick") return;
      if (!Number.isFinite(Number(data.lat)) || !Number.isFinite(Number(data.lon))) return;
      setCoords(Number(data.lat), Number(data.lon), "map");
      localStorage.removeItem("admin_coord_pick");
    } catch (_e) {
      // Ignore JSON/storage errors.
    }
  }

  function init() {
    const latInput = byId("id_vi_do");
    const lonInput = byId("id_kinh_do");
    if (!latInput || !lonInput) return;

    const formEl = latInput.closest("form");
    if (formEl) ensureSourceInput(formEl);

    buildPickUi();

    window.addEventListener("message", function (event) {
      if (event.origin !== window.location.origin) return;
      const data = event.data || {};
      if (data.type !== "admin_coord_pick") return;
      if (!Number.isFinite(Number(data.lat)) || !Number.isFinite(Number(data.lon))) return;
      setCoords(Number(data.lat), Number(data.lon), "map");
    });

    window.addEventListener("focus", tryReadLocalStorageFallback);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
