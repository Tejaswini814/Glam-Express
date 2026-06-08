document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("register-form");
  const url = form.dataset.url;

  form.addEventListener("submit", function (event) {
    event.preventDefault();

    const formData = new FormData(form);
    const csrfToken = document.querySelector(
      "[name=csrfmiddlewaretoken]"
    ).value;

    fetch(url, {
      method: "POST",
      body: formData,
      headers: {
        "X-CSRFToken": csrfToken,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          alert("Registration successful!");
          window.location.href = "/login/"; // or dynamically passed in
        } else {
          alert("Registration failed: " + data.error);
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        alert("Something went wrong.");
      });
  });
});
