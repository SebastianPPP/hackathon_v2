import reflex as rx
from ..state import State


def prize_screen():
    return rx.vstack(
        rx.text("Odbierz nagrodę!", class_name="text-xl font-black text-emerald-400"),
        rx.text("Zakręć kołem i sprawdź co wygrałeś!", class_name="text-xs text-slate-400 text-center"),

        rx.html("""
        <div style="display:flex; flex-direction:column; align-items:center; gap:16px; width:100%">
            <canvas id="wheel" width="280" height="280"></canvas>
            <div id="wynik" style="color:#34d399; font-weight:bold; font-size:1rem; min-height:24px; text-align:center"></div>
            <button id="spinBtn" style="width:100%; background:#059669; color:white; font-weight:bold; padding:12px; border-radius:12px; border:none; cursor:pointer; font-size:1rem;">
                🎰 Zakręć kołem!
            </button>
        </div>

        <script>
        const canvas = document.getElementById('wheel');
        const ctx = canvas.getContext('2d');
        const nagrody = ["Bilet ZTM","Kawa","Sadzonka","100 XP","Torba eko","Niespodzianka","50 XP","Przejazd Mevo"];
        const emoji =   ["🎫","☕","🌱","⭐","🛍️","🎁","💚","🚲"];
        const kolory = ["#064e3b","#065f46","#047857","#059669","#10b981","#34d399","#6ee7b7","#a7f3d0"];
        const n = nagrody.length;
        let kat = 0;
        let obraca = false;

        function rysuj(offset=0) {
            const srodek = 140;
            const r = 130;
            for (let i = 0; i < n; i++) {
                const start = offset + (i * 2 * Math.PI / n);
                const end = offset + ((i+1) * 2 * Math.PI / n);
                ctx.beginPath();
                ctx.moveTo(srodek, srodek);
                ctx.arc(srodek, srodek, r, start, end);
                ctx.fillStyle = kolory[i];
                ctx.fill();
                ctx.strokeStyle = "#0f172a";
                ctx.lineWidth = 2;
                ctx.stroke();

                ctx.save();
                ctx.translate(srodek, srodek);
                ctx.rotate(offset + (i + 0.5) * 2 * Math.PI / n);
                ctx.textAlign = "right";
                ctx.fillStyle = "white";
                ctx.font = "bold 11px sans-serif";
                ctx.fillText(emoji[i] + " " + nagrody[i], r - 8, 4);
                ctx.restore();
            }
            ctx.beginPath();
            ctx.moveTo(srodek + 130, srodek);
            ctx.lineTo(srodek + 115, srodek - 10);
            ctx.lineTo(srodek + 115, srodek + 10);
            ctx.fillStyle = "#f59e0b";
            ctx.fill();
        }

        setTimeout(function() {
            rysuj(0);
            document.getElementById('spinBtn').onclick = function() {
                if (obraca) return;
                obraca = true;
                document.getElementById('wynik').innerText = "";
                const losowy = Math.random() * 2 * Math.PI;
                const obroty = (5 + Math.floor(Math.random() * 5)) * 2 * Math.PI + losowy;
                const start = performance.now();
                const czas = 3000;
                const poczatek = kat;

                function animuj(now) {
                    const t = Math.min((now - start) / czas, 1);
                    const ease = 1 - Math.pow(1 - t, 3);
                    kat = poczatek + obroty * ease;
                    ctx.clearRect(0, 0, 280, 280);
                    rysuj(kat);
                    if (t < 1) {
                        requestAnimationFrame(animuj);
                    } else {
                        obraca = false;
                        const idx = Math.floor(n - ((kat % (2*Math.PI)) / (2*Math.PI)) * n) % n;
                        document.getElementById('wynik').innerText = "Wygrałeś: " + emoji[idx] + " " + nagrody[idx] + "!";
                    }
                }
                requestAnimationFrame(animuj);
            }
        }, 500);
        </script>
        """),

        rx.text(
            f"Twoje punkty: {State.eco_points} XP",
            class_name="text-xs text-slate-400"
        ),

        space="4",
        class_name="w-full px-4 pt-16 pb-24"
    )