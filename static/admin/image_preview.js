(function () {
  function attachPreview(input) {
    if (!input || input.dataset.previewAttached === "1") return;
    input.dataset.previewAttached = "1";

    const holder = document.createElement("div");
    holder.style.marginTop = "10px";

    const img = document.createElement("img");
    img.style.maxWidth = "260px";
    img.style.maxHeight = "260px";
    img.style.display = "none";
    img.style.border = "1px solid #444";
    img.style.borderRadius = "8px";

    holder.appendChild(img);

    // chèn preview ngay dưới input
    input.parentElement.appendChild(holder);

    input.addEventListener("change", function () {
      const file = input.files && input.files[0];
      if (!file) {
        img.style.display = "none";
        img.src = "";
        return;
      }
      img.src = URL.createObjectURL(file);
      img.style.display = "block";
    });
  }

  function init() {
    document.querySelectorAll('input[type="file"]').forEach(attachPreview);
  }

  document.addEventListener("DOMContentLoaded", init);
  document.addEventListener("formset:added", init);
})();
