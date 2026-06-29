"""Shared presentation utilities for reports and timestamps."""

from __future__ import annotations

from datetime import datetime
from io import BytesIO
from textwrap import wrap

from backend.predict import PredictionResult, USD_TO_INR


def current_timestamp() -> str:
    """Return a human-readable local timestamp."""
    return datetime.now().astimezone().strftime("%d %b %Y - %I:%M %p %Z")


def _pdf_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def build_prediction_pdf(
    result: PredictionResult,
    description: str,
    timestamp: str,
) -> bytes:
    """Build a dependency-free, single-page PDF prediction report."""
    lines = [
        ("PriceVision AI", 22),
        ("PRODUCT PRICING REPORT", 10),
        ("", 8),
        (f"Predicted price: ${result.usd:,.2f} USD", 17),
        (f"Approximate conversion: INR {result.inr:,.0f}", 12),
        (f"Conversion rate used: 1 USD = INR {USD_TO_INR:.2f}", 9),
        ("", 8),
        ("Prediction details", 12),
        (f"Generated: {timestamp}", 9),
        (f"Model: {result.model_name}", 9),
        (f"Inference time: {result.elapsed_seconds:.2f} seconds", 9),
        ("", 8),
        ("Product description", 12),
    ]
    lines.extend((line, 9) for line in wrap(description, width=88))
    lines.extend(
        [
            ("", 8),
            (
                "INR value is an approximate conversion from the predicted "
                "USD price.",
                8,
            ),
            (
                "AI-generated estimate for decision support; actual prices "
                "may vary.",
                8,
            ),
        ]
    )

    content = ["BT", "48 770 Td"]
    previous_size = None
    for text, size in lines:
        if size != previous_size:
            content.append(f"/F1 {size} Tf")
            previous_size = size
        content.append(f"({_pdf_escape(text)}) Tj")
        content.append(f"0 -{size + 7} Td")
    content.append("ET")
    stream = "\n".join(content).encode("latin-1", errors="replace")

    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        (
            b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
            b"/Resources << /Font << /F1 5 0 R >> >> "
            b"/Contents 4 0 R >>"
        ),
        b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n"
        + stream
        + b"\nendstream",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ]

    buffer = BytesIO()
    buffer.write(b"%PDF-1.4\n")
    offsets = [0]
    for index, obj in enumerate(objects, start=1):
        offsets.append(buffer.tell())
        buffer.write(f"{index} 0 obj\n".encode())
        buffer.write(obj)
        buffer.write(b"\nendobj\n")
    xref = buffer.tell()
    buffer.write(f"xref\n0 {len(objects) + 1}\n".encode())
    buffer.write(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        buffer.write(f"{offset:010d} 00000 n \n".encode())
    buffer.write(
        (
            f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
            f"startxref\n{xref}\n%%EOF"
        ).encode()
    )
    return buffer.getvalue()
