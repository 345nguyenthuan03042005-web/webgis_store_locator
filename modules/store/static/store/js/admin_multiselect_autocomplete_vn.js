(function () {
  function initProductMultiselect() {
    var select = document.getElementById("id_san_pham");
    if (!select || select.dataset.smartMultiBound === "1" || !select.multiple) return;
    select.dataset.smartMultiBound = "1";

    var wrapper = document.createElement("div");
    wrapper.className = "smart-multi";

    var searchWrap = document.createElement("div");
    searchWrap.className = "smart-multi-search-wrap";

    var searchIcon = document.createElement("span");
    searchIcon.className = "smart-multi-search-icon";
    searchIcon.textContent = "S";

    var searchInput = document.createElement("input");
    searchInput.className = "smart-multi-search";
    searchInput.type = "text";
    searchInput.placeholder = "T\u00ecm nhanh s\u1ea3n ph\u1ea9m...";
    searchInput.autocomplete = "off";
    searchWrap.appendChild(searchIcon);
    searchWrap.appendChild(searchInput);

    var list = document.createElement("div");
    list.className = "smart-multi-list";

    var controls = document.createElement("div");
    controls.className = "smart-multi-controls";

    var btnSingle = document.createElement("button");
    btnSingle.type = "button";
    btnSingle.className = "smart-multi-btn";
    btnSingle.textContent = "Ch\u1ecdn 1";

    var btnMulti = document.createElement("button");
    btnMulti.type = "button";
    btnMulti.className = "smart-multi-btn is-active";
    btnMulti.textContent = "Ch\u1ecdn nhi\u1ec1u";

    var btnAll = document.createElement("button");
    btnAll.type = "button";
    btnAll.className = "smart-multi-btn";
    btnAll.textContent = "Ch\u1ecdn t\u1ea5t c\u1ea3";

    var btnClear = document.createElement("button");
    btnClear.type = "button";
    btnClear.className = "smart-multi-btn";
    btnClear.textContent = "B\u1ecf ch\u1ecdn";

    var summary = document.createElement("span");
    summary.className = "smart-multi-summary";

    controls.appendChild(btnSingle);
    controls.appendChild(btnMulti);
    controls.appendChild(btnAll);
    controls.appendChild(btnClear);
    controls.appendChild(summary);

    var hint = document.createElement("div");
    hint.className = "smart-multi-hint";
    hint.textContent = "Ch\u1ebf \u0111\u1ed9 Ch\u1ecdn nhi\u1ec1u: nh\u1ea5n gi\u1eef chu\u1ed9t v\u00e0 k\u00e9o \u1edf b\u1ea5t k\u1ef3 v\u1ecb tr\u00ed trong khung danh s\u00e1ch.";

    var parent = select.parentNode;
    parent.insertBefore(wrapper, select);
    wrapper.appendChild(searchWrap);
    wrapper.appendChild(list);
    wrapper.appendChild(controls);
    wrapper.appendChild(hint);

    select.classList.add("smart-multi-select");
    select.style.display = "none";

    var mode = "multi";
    var isDragging = false;
    var dragSetValue = true;
    var lastIndex = -1;
    var rows = [];

    function createRows() {
      rows = [];
      list.innerHTML = "";
      for (var i = 0; i < select.options.length; i += 1) {
        var opt = select.options[i];
        var row = document.createElement("div");
        row.className = "smart-multi-row";
        row.textContent = opt.text;
        row.dataset.index = String(i);
        row.dataset.text = opt.text.toLowerCase();
        list.appendChild(row);
        rows.push(row);
      }
    }

    function visibleRows() {
      var arr = [];
      for (var i = 0; i < rows.length; i += 1) {
        if (!rows[i].classList.contains("is-hidden")) arr.push(rows[i]);
      }
      return arr;
    }

    function syncRowClasses() {
      for (var i = 0; i < rows.length; i += 1) {
        rows[i].classList.toggle("is-selected", !!select.options[i].selected);
      }
    }

    function updateSummary() {
      var selected = 0;
      for (var i = 0; i < select.options.length; i += 1) {
        if (select.options[i].selected) selected += 1;
      }
      summary.textContent =
        "\u0110\u00e3 ch\u1ecdn: " +
        selected +
        " | Hi\u1ec3n th\u1ecb: " +
        visibleRows().length +
        " | T\u1ed5ng: " +
        select.options.length;
    }

    function triggerChange() {
      select.dispatchEvent(new Event("change", { bubbles: true }));
      syncRowClasses();
      updateSummary();
    }

    function setMode(nextMode) {
      mode = nextMode;
      isDragging = false;
      lastIndex = -1;

      if (mode === "single") {
        var first = -1;
        for (var i = 0; i < select.options.length; i += 1) {
          if (select.options[i].selected) {
            first = i;
            break;
          }
        }
        for (var j = 0; j < select.options.length; j += 1) {
          select.options[j].selected = j === first;
        }
        triggerChange();
      }

      btnSingle.classList.toggle("is-active", mode === "single");
      btnMulti.classList.toggle("is-active", mode === "multi");
    }

    function getIndexFromPoint(clientY) {
      var visible = visibleRows();
      if (!visible.length) return -1;

      var rect = list.getBoundingClientRect();
      var y = clientY - rect.top + list.scrollTop;
      if (y < 0) y = 0;
      var maxY = Math.max(0, list.scrollHeight - 1);
      if (y > maxY) y = maxY;

      var rowHeight = visible[0].offsetHeight || 30;
      var pos = Math.floor(y / rowHeight);
      if (pos < 0) pos = 0;
      if (pos >= visible.length) pos = visible.length - 1;
      return parseInt(visible[pos].dataset.index, 10);
    }

    function applyIndex(index) {
      if (index < 0 || index >= select.options.length) return;
      if (index === lastIndex) return;
      lastIndex = index;

      if (mode === "single") {
        for (var i = 0; i < select.options.length; i += 1) {
          select.options[i].selected = i === index;
        }
      } else if (select.options[index].selected !== dragSetValue) {
        select.options[index].selected = dragSetValue;
      } else {
        return;
      }
      triggerChange();
    }

    function filterRows() {
      var q = searchInput.value.trim().toLowerCase();
      for (var i = 0; i < rows.length; i += 1) {
        var matched = !q || rows[i].dataset.text.indexOf(q) !== -1;
        rows[i].classList.toggle("is-hidden", !matched);
      }
      updateSummary();
    }

    list.addEventListener("mousedown", function (event) {
      event.preventDefault();
      var index = getIndexFromPoint(event.clientY);
      if (index < 0) return;

      if (mode === "single") {
        isDragging = false;
        lastIndex = -1;
        applyIndex(index);
      } else {
        dragSetValue = !select.options[index].selected;
        isDragging = true;
        lastIndex = -1;
        applyIndex(index);
      }
      list.focus();
    });

    document.addEventListener("mousemove", function (event) {
      if (!isDragging || mode !== "multi") return;
      var rect = list.getBoundingClientRect();
      if (event.clientX < rect.left || event.clientX > rect.right) return;
      var index = getIndexFromPoint(event.clientY);
      applyIndex(index);
    });

    document.addEventListener("mouseup", function () {
      isDragging = false;
      lastIndex = -1;
    });

    btnSingle.addEventListener("click", function () {
      setMode("single");
    });

    btnMulti.addEventListener("click", function () {
      setMode("multi");
    });

    btnAll.addEventListener("click", function () {
      var visible = visibleRows();
      for (var i = 0; i < visible.length; i += 1) {
        var index = parseInt(visible[i].dataset.index, 10);
        select.options[index].selected = true;
      }
      triggerChange();
    });

    btnClear.addEventListener("click", function () {
      for (var i = 0; i < select.options.length; i += 1) {
        select.options[i].selected = false;
      }
      triggerChange();
    });

    searchInput.addEventListener("input", filterRows);

    createRows();
    syncRowClasses();
    updateSummary();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initProductMultiselect);
  } else {
    initProductMultiselect();
  }
})();
