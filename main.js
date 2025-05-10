// گرفتن فرم از DOM
const loginForm = document.getElementById('loginForm');

// جلوگیری از ارسال فرم و گرفتن اطلاعات
loginForm.addEventListener('submit', function (e) {
  e.preventDefault(); // جلوگیری از ارسال واقعی

  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;

  console.log('📧 ایمیل:', email);
  console.log('🔑 رمز عبور:', password);

  // می‌تونی اینجا بررسی امنیتی هم انجام بدی
  alert('اطلاعات فرم در کنسول چاپ شد.');
});
