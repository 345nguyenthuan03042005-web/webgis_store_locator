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
      status.textContent = "Nguon toa do: ban do (do chinh xac cao).";
    } else if (source === "address_pending") {
      status.textContent = "Da tim duoc vi tri gan dung tu dia chi. Toa do hien tai chua doi; ban phai click tren ban do de chot.";
    } else {
      status.textContent = "";
    }
  }

  function setAddressPending(lat, lon) {
    setSource("address_pending");
    const status = byId("coord-source-status");
    if (status && Number.isFinite(lat) && Number.isFinite(lon)) {
      status.textContent =
        "Da tim duoc vi tri gan dung: " +
        Number(lat).toFixed(6) +
        ", " +
        Number(lon).toFixed(6) +
        ". Toa do hien tai chua doi; ban phai click tren ban do de chot.";
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
          "Trinh duyet dang chan popup map. Bam OK de mo map trong cung tab."
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
      input.title = "Khong duoc nhap truc tiep. Hay lay tu dia chi hoac ban do.";
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
          window.alert("Vui long nhap dia chi truoc.");
          return;
        }
        geocodeBtn.disabled = true;
        try {
          const found = await geocodeAddress(query);
          if (!found || !Number.isFinite(found.lat) || !Number.isFinite(found.lon)) {
            window.alert("Khong tim thay toa do tu dia chi. Thu rut gon dia chi (bo ten toa nha/cao oc) roi thu lai.");
            return;
          }
          // Do not overwrite saved coordinates with approximate geocode.
          // Geocode is only used to center the map for manual confirmation.
          setAddressPending(found.lat, found.lon);
          openPickMap(found.lat, found.lon);
        } catch (_e) {
          window.alert("Khong the lay toa do tu dia chi luc nay.");
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
