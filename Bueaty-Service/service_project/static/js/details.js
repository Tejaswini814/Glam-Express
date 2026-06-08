document.addEventListener("DOMContentLoaded", function () {
  const bookingForm = document.getElementById("bookingForm");
  const errorDiv = document.getElementById("formError");
  const bookingModal = document.getElementById("bookingModal");

  window.openBookingModal = function () {
    if (bookingModal) bookingModal.style.display = "flex";
    if (bookingForm) bookingForm.reset();
    if (errorDiv) errorDiv.textContent = "";
  };

  window.closeBookingModal = function () {
    if (bookingModal) bookingModal.style.display = "none";
  };

  if (bookingForm) {
    const url = bookingForm.dataset.url;

    bookingForm.addEventListener("submit", function (e) {
      e.preventDefault();

      const submitBtn = bookingForm.querySelector('button[type="submit"]');
      if (!submitBtn) return;

      submitBtn.disabled = true;
      submitBtn.textContent = "Booking...";
      if (errorDiv) errorDiv.textContent = "";

      const formData = new FormData();
      formData.append("parlour_id", bookingForm.querySelector("[name=parlour_id]").value);
      formData.append("location", bookingForm.querySelector("[name=location]").value);
      formData.append("date", bookingForm.querySelector("[name=date]").value);
      formData.append("time", bookingForm.querySelector("[name=time]").value);

      const services = bookingForm.querySelector("[name=services]");
      if (services && services.selectedOptions) {
        Array.from(services.selectedOptions).forEach(option => {
          formData.append("services", option.value);
        });
      }

      const csrfTokenInput = bookingForm.querySelector("[name=csrfmiddlewaretoken]");
      const csrfToken = csrfTokenInput ? csrfTokenInput.value : "";

      fetch(url, {
        method: "POST",
        headers: {
          "X-CSRFToken": csrfToken,
        },
        body: formData,
      })
        .then(res => res.json())
        .then(data => {
          submitBtn.disabled = false;
          submitBtn.textContent = "Book Now";

          if (data.status === "success") {
            window.location.href = data.redirect_url;
          } else {
            if (errorDiv) errorDiv.textContent = data.message || "Booking failed.";
          }
        })
        .catch(() => {
          submitBtn.disabled = false;
          submitBtn.textContent = "Book Now";
          if (errorDiv) errorDiv.textContent = "Something went wrong. Please try again.";
        });
    });
  }
});