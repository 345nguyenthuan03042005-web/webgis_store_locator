document.addEventListener("DOMContentLoaded", () => {
  const panels = document.querySelectorAll(".panel, .card");
  panels.forEach((el, idx) => {
    el.classList.add("fade-up");
    el.style.animationDelay = `${Math.min(idx * 0.05, 0.35)}s`;
  });

  const isMobile = window.matchMedia("(max-width: 1080px)").matches;
  if (isMobile) {
    document.querySelectorAll(".menu a.active").forEach((link) => {
      link.scrollIntoView({ block: "nearest", inline: "nearest" });
    });
  }

  document.querySelectorAll("input[type='file']").forEach((input) => {
    input.addEventListener("change", (event) => {
      const file = event.target.files && event.target.files[0];
      const preview = document.querySelector(`img[data-preview-for='${input.id}']`);
      if (!preview) return;
      if (!file || !file.type || !file.type.startsWith("image/")) return;

      preview.src = URL.createObjectURL(file);
      preview.classList.remove("is-hidden");
    });
  });

  // Better UX for long multi-select fields (e.g. San pham in Cua hang form)
  document.querySelectorAll("form select[multiple]").forEach((selectEl) => {
    if (!selectEl.id) return;

    const row = selectEl.closest(".form-row");
    if (!row) return;
    row.classList.add("multi-row");

    const box = document.createElement("div");
    box.className = "multi-select-box";
    box.innerHTML = `
      <div class="multi-select-tools">
        <input type="text" class="multi-search" placeholder="Tìm nhanh sản phẩm..." aria-label="Tìm nhanh sản phẩm">
        <div class="multi-actions">
          <button type="button" class="multi-btn" data-action="all">Chọn tất cả</button>
          <button type="button" class="multi-btn" data-action="clear">Bỏ chọn</button>
        </div>
      </div>
      <div class="multi-meta">Đã chọn <strong class="multi-count">0</strong> mục</div>
    `;

    selectEl.parentNode.insertBefore(box, selectEl);
    box.appendChild(selectEl);
    selectEl.classList.add("enhanced-multi");

    const searchInput = box.querySelector(".multi-search");
    const countNode = box.querySelector(".multi-count");

    const updateCount = () => {
      const count = Array.from(selectEl.options).filter((o) => o.selected).length;
      countNode.textContent = String(count);
    };

    const filterOptions = (keyword) => {
      const q = (keyword || "").trim().toLowerCase();
      Array.from(selectEl.options).forEach((opt) => {
        const visible = !q || opt.text.toLowerCase().includes(q);
        opt.hidden = !visible;
      });
    };

    box.querySelectorAll(".multi-btn").forEach((btn) => {
      btn.addEventListener("click", () => {
        const action = btn.getAttribute("data-action");
        if (action === "all") {
          Array.from(selectEl.options).forEach((opt) => {
            if (!opt.hidden && !opt.disabled) opt.selected = true;
          });
        } else {
          Array.from(selectEl.options).forEach((opt) => {
            if (!opt.hidden) opt.selected = false;
          });
        }
        updateCount();
        selectEl.dispatchEvent(new Event("change", { bubbles: true }));
      });
    });

    searchInput.addEventListener("input", () => filterOptions(searchInput.value));
    selectEl.addEventListener("change", updateCount);
    updateCount();
  });

  // CuaHang coordinate picker integration (from store/home map click)
  const pickBtn = document.getElementById("btn-pick-coord");
  if (pickBtn) {
    const latInput = document.getElementById(pickBtn.dataset.latField || "id_vi_do");
    const lonInput = document.getElementById(pickBtn.dataset.lonField || "id_kinh_do");
    const sourceInput = document.getElementById(pickBtn.dataset.sourceField || "id_coord_from_map");

    if (latInput) {
      latInput.readOnly = true;
      latInput.title = "Tọa độ chỉ được lấy từ bản đồ.";
    }
    if (lonInput) {
      lonInput.readOnly = true;
      lonInput.title = "Tọa độ chỉ được lấy từ bản đồ.";
    }

    const applyPickedCoord = (payload) => {
      if (!payload || payload.type !== "admin_coord_pick") return;
      if (!latInput || !lonInput || !sourceInput) return;

      const lat = Number(payload.lat);
      const lon = Number(payload.lon);
      if (!Number.isFinite(lat) || !Number.isFinite(lon)) return;

      latInput.value = lat.toFixed(6);
      lonInput.value = lon.toFixed(6);
      sourceInput.value = "map";
    };

    const consumePickedCoordFromStorage = () => {
      try {
        const saved = localStorage.getItem("admin_coord_pick");
        if (!saved) return;
        applyPickedCoord(JSON.parse(saved));
        localStorage.removeItem("admin_coord_pick");
      } catch (_e) {
        // ignore parse/storage errors
      }
    };

    window.addEventListener("message", (event) => {
      if (!event || !event.data) return;
      applyPickedCoord(event.data);
    });

    window.addEventListener("storage", (event) => {
      if (event.key === "admin_coord_pick") {
        consumePickedCoordFromStorage();
      }
    });
    window.addEventListener("focus", consumePickedCoordFromStorage);
    window.addEventListener("pageshow", consumePickedCoordFromStorage);
    consumePickedCoordFromStorage();
    // Fallback: some browsers/tabs miss storage/message delivery timing.
    const coordPoller = window.setInterval(consumePickedCoordFromStorage, 1200);
    window.addEventListener("beforeunload", () => window.clearInterval(coordPoller));

    pickBtn.addEventListener("click", (event) => {
      event.preventDefault();
      const baseUrl = pickBtn.getAttribute("href") || "/";
      const url = new URL(baseUrl, window.location.origin);

      const addressInput = document.getElementById("id_dia_chi");
      const address = addressInput ? addressInput.value.trim() : "";
      if (address) {
        url.searchParams.set("q", address);
      }

      if (latInput && lonInput && latInput.value && lonInput.value) {
        // Keep current saved point as initial map center.
        url.searchParams.set("center_lat", latInput.value);
        url.searchParams.set("center_lon", lonInput.value);
      }

      // Keep opener so map tab can postMessage coordinates back immediately.
      window.open(url.toString(), "_blank");
    });
  }
});
