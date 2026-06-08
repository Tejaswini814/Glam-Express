document.addEventListener("DOMContentLoaded", function () {
  const reviewForm = document.getElementById("reviewForm");
  if (!reviewForm) return;

  reviewForm.addEventListener("submit", function (e) {
    e.preventDefault();

    const form = e.target;
    const formData = new FormData(form);
    const csrfToken = form.querySelector("[name=csrfmiddlewaretoken]").value;
    const redirectUrl = form.dataset.redirectUrl;

    fetch("", {
      method: "POST",
      headers: {
        "X-CSRFToken": csrfToken,
      },
      body: formData,
    })
      .then((res) => res.json())
      .then((data) => {
        const msg = document.getElementById("responseMessage");
        msg.style.color = data.status === "success" ? "green" : "red";
        msg.textContent = data.message;

        if (data.status === "success" && redirectUrl) {
          setTimeout(() => {
            window.location.href = redirectUrl;
          }, 2000);
        }
      })
      .catch(() => {
        const msg = document.getElementById("responseMessage");
        msg.style.color = "red";
        msg.textContent = "An error occurred. Please try again.";
      });
  });
});
