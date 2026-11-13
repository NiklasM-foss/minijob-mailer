import "dotenv/config";
import nodemailer from "nodemailer";

async function sendeSmtp(konto, mail) {
  const transporter = nodemailer.createTransport({
    host: konto.host,
    port: konto.port,
    secure: konto.port === 465,
    auth: { user: konto.user, pass: konto.passwort },
  });

  const info = await transporter.sendMail({
    from: konto.user,
    to: mail.empfaenger,
    subject: mail.betreff,
    text: mail.text,
  });

  return info.messageId;
}

const konto = {
  host: "smtp.gmail.com",
  port: 465,
  user: process.env.SMTP_USER,
  passwort: process.env.SMTP_PASS,
};

const mail = {
  empfaenger: process.env.SMTP_USER,
  betreff: "Test",
  text: "Hallo, das ist ein Test.",
};
console.log("User:", process.env.SMTP_USER, "| Pass gesetzt:", !!process.env.SMTP_PASS);
try {
  const id = await sendeSmtp(konto, mail);
  console.log("Gesendet:", id);
} catch (err) {
  console.error("Fehler:", err.message);
}