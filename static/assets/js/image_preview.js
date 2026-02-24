(function () {
  function isAvatarField(input) {
    return (input.name || "").toLowerCase().includes("avatar");
  }

  function mediaFallback(input) {
    if (isAvatarField(input)) return "/media/avatar/default.png";
    return "";
  }

  function findCurrentImage(input) {
    const wrap =
      input.closest(".form-row, .fieldBox, .aligned") || input.parentElement;

    if (wrap) {
      const a = wrap.querySelector('a[href^="/media/"]');
      if (a) return a.getAttribute("href");
    }
    return mediaFallback(input);
  }

  function attachPreview(input) {
    if (!input || input.type !== "file" || input.dataset.previewAttached) return;
    input.dataset.previewAttached = "1";

    const holder = document.createElement("div");
    holder.style.marginTop = "10px";

    const img = document.createElement("img");
    img.style.maxWidth = "260px";
    img.style.maxHeight = "260px";
    img.style.display = "none";
    img.style.border = "1px solid rgba(255,255,255,.18)";
    img.style.borderRadius = "10px";
    img.style.objectFit = "cover";

    holder.appendChild(img);
    input.parentElement.appendChild(holder);

    // hiện ảnh cũ (edit) hoặc default avatar
    const current = findCurrentImage(input);
    if (current) {
      img.src = current;
      img.style.display = "block";
    }

    input.addEventListener("change", () => {
      const file = input.files && input.files[0];
      if (file) {
        img.src = URL.createObjectURL(file);
        img.style.display = "block";
      }
    });
  }

  function init() {
    document.querySelectorAll('input[type="file"]').forEach(attachPreview);
  }

  document.addEventListener("DOMContentLoaded", init);
  document.addEventListener("formset:added", init);
})();
