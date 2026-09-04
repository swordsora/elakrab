/*
 * إعداد قاعدة البيانات المركزية — عدّل هذا الملف فقط عند تغيير الخادم.
 *
 * الوضع الافتراضي: custom-rest
 * يجب أن يوفّر الخادم نفس المسارات التي يستخدمها التطبيق:
 * /login و /heartbeat و /qr-login و /devices و /devices/block-self
 * /accounts/sync وغيرها من المسارات الموجودة في app.js.
 *
 * قاعدة محلية خاصة بك:
 * غيّر baseUrl إلى عنوان الـ API المحلي، مثل:
 * baseUrl: 'http://192.168.1.20:3000/api/local'
 *
 * Supabase أو Firebase:
 * الأفضل إنشاء Edge Function / Cloud Function أو API Gateway يحافظ على
 * نفس عقد المسارات السابقة، ثم ضع عنوانه في baseUrl. لا تضع مفاتيح سرية
 * هنا؛ هذا الملف يصل إلى أجهزة المستخدمين. عند الحاجة إلى تحويل مختلف
 * تمامًا، عرّف request(path, options, context) وأعد Response JSON متوافقًا.
 * هذا هو المكان المخصص لتعديل ربط قاعدة البيانات المركزية فقط.
 */
window.TAWOOS_CENTRAL_CONFIG = {
  provider: 'custom-rest',
  baseUrl: 'https://3000-icvfeaxb8zgobmqlkioua-a3ed9d5f.us3.manus.computer/api/local',
  timeoutMs: 8000,
  headers: { 'Content-Type': 'application/json' }
  // مثال محول مخصص:
  // request: async (path, options, context) => {
  //   const response = await fetch(`https://your-gateway.example${path}`, options);
  //   return response.json();
  // }
};
