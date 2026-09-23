document.addEventListener("DOMContentLoaded", () => {

    const header = document.getElementById("site-header");
    const menuToggle = document.getElementById("menu-toggle");
    const mainNav = document.getElementById("main-nav");

    // =====================================================
    // HEADER
    // =====================================================

    if (header) {

        const updateHeader = () => {
            header.classList.toggle(
                "scrolled",
                window.scrollY > 50
            );
        };

        updateHeader();

        window.addEventListener(
            "scroll",
            updateHeader,
            { passive: true }
        );
    }


    // =====================================================
    // MENÚ MÓVIL
    // =====================================================

    if (menuToggle && mainNav) {

        menuToggle.addEventListener("click", () => {

            const open =
                mainNav.classList.toggle("active");

            menuToggle.setAttribute(
                "aria-expanded",
                String(open)
            );
        });


        document
            .querySelectorAll(".main-nav a")
            .forEach((link) => {

                link.addEventListener("click", () => {

                    mainNav.classList.remove("active");

                    menuToggle.setAttribute(
                        "aria-expanded",
                        "false"
                    );
                });

            });
    }


    // =====================================================
    // MODAL DE RESERVA
    // =====================================================

    const modal =
        document.getElementById("appointment-modal");

    const openButtons =
        document.querySelectorAll(".js-open-appointment");

    const closeButtons =
        document.querySelectorAll(".js-close-appointment");


    const openAppointment = () => {

        if (!modal) return;

        modal.classList.add("is-open");

        modal.setAttribute(
            "aria-hidden",
            "false"
        );

        document.body.classList.add(
            "modal-open"
        );
    };


    const closeAppointment = () => {

        if (!modal) return;

        modal.classList.remove("is-open");

        modal.setAttribute(
            "aria-hidden",
            "true"
        );

        document.body.classList.remove(
            "modal-open"
        );
    };


    openButtons.forEach((button) => {

        button.addEventListener(
            "click",
            (event) => {

                event.preventDefault();

                openAppointment();

            }
        );

    });


    closeButtons.forEach((button) => {

        button.addEventListener(
            "click",
            closeAppointment
        );

    });


    document.addEventListener(
        "keydown",
        (event) => {

            if (event.key === "Escape") {
                closeAppointment();
            }

        }
    );


    // =====================================================
    // ELEMENTOS DEL FORMULARIO
    // =====================================================

    const medicoSelect =
        document.getElementById("medico");

    const fechaSelect =
        document.getElementById("fecha");

    const horaSelect =
        document.getElementById("hora");


    if (
        !medicoSelect ||
        !fechaSelect ||
        !horaSelect
    ) {
        return;
    }


    // =====================================================
    // REINICIAR SELECT
    // =====================================================

    const resetSelect = (
        select,
        text
    ) => {

        select.innerHTML = "";

        const option =
            document.createElement("option");

        option.value = "";

        option.textContent = text;

        select.appendChild(option);

        select.disabled = true;
    };


    // =====================================================
    // CARGAR HORAS
    // =====================================================
    const formatearHora = (hora) => {
        const [horas, minutos] = hora.split(":");

        let h = parseInt(horas, 10);

        const periodo = h >= 12 ? "PM" : "AM";

        if (h === 0) {
            h = 12;
        } else if (h > 12) {
            h -= 12;
        }

        return `${h}:${minutos} ${periodo}`;
    };

    // =====================================================
    // CONVERTIR HORA 24H → AM/PM
    // =====================================================

    const convertirHoraAMPM = (hora) => {

        if (!hora) {
            return "";
        }

        const partes = hora.split(":");

        const hora24 = parseInt(partes[0], 10);
        const minutos = partes[1];

        const periodo = hora24 >= 12
            ? "PM"
            : "AM";

        let hora12 = hora24 % 12;

        if (hora12 === 0) {
            hora12 = 12;
        }

        return `${String(hora12).padStart(2, "0")}:${minutos} ${periodo}`;
    };

    const loadHours = async () => {

        const medicoId =
            medicoSelect.value;

        const fecha =
            fechaSelect.value;


        resetSelect(
            horaSelect,
            "Cargando horas disponibles..."
        );


        if (!medicoId || !fecha) {

            resetSelect(
                horaSelect,
                "Selecciona una fecha primero"
            );

            return;
        }


        try {

            const response = await fetch(
                `/citas/api/horas/${medicoId}/?fecha=${encodeURIComponent(fecha)}`,
                {
                    headers: {
                        "X-Requested-With":
                            "XMLHttpRequest"
                    }
                }
            );


            if (!response.ok) {

                throw new Error(
                    "No se pudieron cargar las horas."
                );
            }


            const data =
                await response.json();


            if (
                !data.horas ||
                !data.horas.length
            ) {

                resetSelect(
                    horaSelect,
                    "No hay horas disponibles"
                );

                return;
            }


            horaSelect.innerHTML = "";

            const placeholder = document.createElement("option");
            placeholder.value = "";
            placeholder.textContent = "Selecciona una hora";
            placeholder.selected = true;

            horaSelect.appendChild(placeholder);

            data.horas.forEach((hora) => {

                const option =
                    document.createElement("option");

                option.value = hora;

                option.textContent = convertirHoraAMPM(hora);

                horaSelect.appendChild(option);

            });


            horaSelect.disabled = false;


        } catch (error) {

            console.error(error);

            resetSelect(
                horaSelect,
                "No se pudieron cargar las horas"
            );

        }
    };


    // =====================================================
    // CARGAR FECHAS
    // =====================================================

    const loadDates = async (
        medicoId
    ) => {

        resetSelect(
            fechaSelect,
            "Cargando fechas disponibles..."
        );


        resetSelect(
            horaSelect,
            "Selecciona una fecha primero"
        );


        if (!medicoId) {

            resetSelect(
                fechaSelect,
                "Selecciona un médico primero"
            );

            return;
        }


        try {

            const response = await fetch(
                `/citas/api/fechas/${medicoId}/`,
                {
                    headers: {
                        "X-Requested-With":
                            "XMLHttpRequest"
                    }
                }
            );


            if (!response.ok) {

                throw new Error(
                    "No se pudieron cargar las fechas."
                );
            }


            const data =
                await response.json();


            if (
                !data.fechas ||
                !data.fechas.length
            ) {

                resetSelect(
                    fechaSelect,
                    "No hay fechas disponibles"
                );

                return;
            }


            fechaSelect.innerHTML = "";


            data.fechas.forEach((item) => {

                const option =
                    document.createElement("option");

                option.value =
                    item.fecha;

                option.textContent =
                    `${item.dia || ""}${item.dia ? " · " : ""}${item.texto}`;

                fechaSelect.appendChild(option);

            });


            fechaSelect.disabled = false;

            fechaSelect.value = "";


        } catch (error) {

            console.error(error);

            resetSelect(
                fechaSelect,
                "No se pudieron cargar las fechas"
            );

        }
    };


    // =====================================================
    // CAMBIO DE MÉDICO
    // =====================================================

    medicoSelect.addEventListener(
        "change",
        () => {

            loadDates(
                medicoSelect.value
            );

        }
    );


    // =====================================================
    // CAMBIO DE FECHA
    // =====================================================

    fechaSelect.addEventListener(
        "change",
        loadHours
    );


    // =====================================================
    // MÉDICO SELECCIONADO DESDE LA URL
    // =====================================================

    const params =
        new URLSearchParams(
            window.location.search
        );

    const medicoDesdeUrl =
        params.get("medico");


    const hasAppointmentMessage =
        Boolean(
            document.querySelector(
                ".appointment-messages .alert"
            )
        );


    if (medicoDesdeUrl) {

        const option =
            Array.from(
                medicoSelect.options
            ).find(
                (option) =>
                    option.value ===
                    medicoDesdeUrl
            );


        if (option) {

            // Seleccionar médico
            medicoSelect.value =
                medicoDesdeUrl;


            // Abrir formulario
            openAppointment();


            // Cargar fechas
            loadDates(
                medicoDesdeUrl
            );


            // Limpiar la URL
            history.replaceState(
                {},
                document.title,
                window.location.pathname +
                window.location.hash
            );
        }

    } else if (hasAppointmentMessage) {

        openAppointment();

    }


    // =====================================================
    // SOBRE NOSOTROS - CARRUSEL
    // =====================================================

    const aboutCarousel =
        document.getElementById(
            "about-carousel"
        );


    if (aboutCarousel) {

        const slides =
            Array.from(
                aboutCarousel.querySelectorAll(
                    ".about-slide"
                )
            );

        const dots =
            Array.from(
                aboutCarousel.querySelectorAll(
                    ".about-dot"
                )
            );


        let currentSlide = 0;

        let carouselTimer = null;


        const showSlide = (
            index
        ) => {

            if (slides.length <= 1) {
                return;
            }


            currentSlide =
                (index + slides.length) %
                slides.length;


            slides.forEach(
                (slide, i) => {

                    slide.classList.toggle(
                        "is-active",
                        i === currentSlide
                    );

                }
            );


            dots.forEach(
                (dot, i) => {

                    dot.classList.toggle(
                        "is-active",
                        i === currentSlide
                    );

                    dot.setAttribute(
                        "aria-selected",
                        i === currentSlide
                            ? "true"
                            : "false"
                    );

                }
            );

        };


        const restartCarousel = () => {

            if (carouselTimer) {
                clearInterval(
                    carouselTimer
                );
            }


            if (slides.length > 1) {

                carouselTimer =
                    setInterval(
                        () => {

                            showSlide(
                                currentSlide + 1
                            );

                        },
                        5000
                    );
            }

        };


        dots.forEach(
            (dot, index) => {

                dot.addEventListener(
                    "click",
                    () => {

                        showSlide(index);

                        restartCarousel();

                    }
                );

            }
        );


        showSlide(0);

        restartCarousel();


        aboutCarousel.addEventListener(
            "mouseenter",
            () => {

                if (carouselTimer) {

                    clearInterval(
                        carouselTimer
                    );

                }

            }
        );


        aboutCarousel.addEventListener(
            "mouseleave",
            restartCarousel
        );

    }

});