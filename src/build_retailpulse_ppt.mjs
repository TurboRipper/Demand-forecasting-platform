import fs from "node:fs/promises";
import path from "node:path";

import * as artifactTool from "file:///C:/Users/Tharuneesh/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs";

const {
  Presentation,
  PresentationFile,
  column,
  row,
  grid,
  layers,
  panel,
  text,
  shape,
  chart,
  rule,
  fill,
  hug,
  wrap,
  fixed,
  fr,
  auto,
  grow,
} = artifactTool;

const outputDir = path.resolve("output");
const previewDir = path.resolve("scratch", "previews");

await fs.mkdir(outputDir, { recursive: true });
await fs.mkdir(previewDir, { recursive: true });

const deck = Presentation.create({
  slideSize: { width: 1920, height: 1080 },
});

const colors = {
  navy: "#0A1628",
  blue: "#175CD3",
  cyan: "#12B3A8",
  sky: "#DBEAFE",
  mint: "#DFF8F3",
  amber: "#F5B546",
  coral: "#F97066",
  white: "#F8FAFC",
  ink: "#10233C",
  slate: "#556274",
  soft: "#EEF4F8",
  border: "#C9D7E3",
};

function slideBase(slide, content) {
  slide.compose(
    layers(
      { name: "root", width: fill, height: fill },
      [
        shape({
          name: "bg",
          x: 0,
          y: 0,
          width: 1920,
          height: 1080,
          shape: "rect",
          fill: colors.soft,
        }),
        shape({
          name: "accent-top",
          x: 0,
          y: 0,
          width: 1920,
          height: 180,
          shape: "rect",
          fill: "#E6F4FF",
        }),
        content,
      ],
    ),
    { frame: { left: 0, top: 0, width: 1920, height: 1080 }, baseUnit: 8 },
  );
}

function titleBlock(title, subtitle, width = 1240) {
  return column(
    { name: "title-block", width: fill, height: hug, gap: 14 },
    [
      text(title, {
        name: "slide-title",
        width: wrap(width),
        height: hug,
        style: { fontSize: 48, bold: true, color: colors.ink, fontFace: "Aptos Display" },
      }),
      text(subtitle, {
        name: "slide-subtitle",
        width: wrap(width),
        height: hug,
        style: { fontSize: 22, color: colors.slate, fontFace: "Aptos" },
      }),
    ],
  );
}

function bulletCard(title, bullets, tone = colors.white) {
  return panel(
    {
      name: title.toLowerCase().replace(/\s+/g, "-"),
      width: fill,
      height: fill,
      padding: 28,
      borderRadius: 24,
      fill: tone,
      stroke: colors.border,
    },
    column(
      { width: fill, height: fill, gap: 16 },
      [
        text(title, {
          width: fill,
          height: hug,
          style: { fontSize: 28, bold: true, color: colors.ink, fontFace: "Aptos Display" },
        }),
        ...bullets.map((item, index) =>
          row(
            { width: fill, height: hug, gap: 14 },
            [
              shape({
                name: `dot-${index}`,
                width: fixed(12),
                height: fixed(12),
                shape: "ellipse",
                fill: colors.blue,
              }),
              text(item, {
                width: fill,
                height: hug,
                style: { fontSize: 21, color: colors.slate, fontFace: "Aptos" },
              }),
            ],
          ),
        ),
      ],
    ),
  );
}

function metricCard(label, value, accent) {
  return panel(
    {
      width: fill,
      height: fill,
      padding: 24,
      borderRadius: 22,
      fill: colors.white,
      stroke: colors.border,
    },
    column(
      { width: fill, height: fill, gap: 10 },
      [
        text(label, {
          width: fill,
          height: hug,
          style: { fontSize: 18, color: colors.slate, fontFace: "Aptos" },
        }),
        text(value, {
          width: fill,
          height: hug,
          style: { fontSize: 34, bold: true, color: accent, fontFace: "Aptos Display" },
        }),
      ],
    ),
  );
}

function addFooter(content, slideNumber) {
  return row(
    { name: "footer", width: fill, height: hug, gap: 12 },
    [
      text(content, {
        name: "footer-text",
        width: fill,
        height: hug,
        style: { fontSize: 14, color: colors.slate, fontFace: "Aptos" },
      }),
      text(String(slideNumber), {
        name: "page",
        width: fixed(24),
        height: hug,
        style: { fontSize: 14, color: colors.slate, fontFace: "Aptos", align: "right" },
      }),
    ],
  );
}

// Slide 1
{
  const slide = deck.slides.add();
  slideBase(
    slide,
    column(
      { width: fill, height: fill, padding: { x: 92, y: 78 }, gap: 28 },
      [
        text("RetailPulse ML", {
          name: "cover-title",
          width: wrap(1100),
          height: hug,
          style: { fontSize: 70, bold: true, color: colors.navy, fontFace: "Aptos Display" },
        }),
        text("Containerized Demand Forecasting Platform", {
          name: "cover-subtitle",
          width: wrap(980),
          height: hug,
          style: { fontSize: 32, color: colors.blue, fontFace: "Aptos Display" },
        }),
        text(
          "Easy demo project for predicting retail demand, checking stockout risk, and giving replenishment actions using Docker, machine learning, and agentic AI.",
          {
            name: "cover-body",
            width: wrap(980),
            height: hug,
            style: { fontSize: 24, color: colors.slate, fontFace: "Aptos" },
          },
        ),
        row(
          { width: fill, height: fixed(420), gap: 24 },
          [
            panel(
              {
                width: grow(1.2),
                height: fill,
                padding: 34,
                borderRadius: 30,
                fill: colors.navy,
              },
              column(
                { width: fill, height: fill, gap: 20 },
                [
                  text("What the system does", {
                    width: fill,
                    height: hug,
                    style: { fontSize: 28, bold: true, color: colors.white, fontFace: "Aptos Display" },
                  }),
                  text("Forecasts demand", {
                    width: fill,
                    height: hug,
                    style: { fontSize: 24, color: colors.sky, fontFace: "Aptos" },
                  }),
                  text("Detects unusual sales spikes", {
                    width: fill,
                    height: hug,
                    style: { fontSize: 24, color: colors.sky, fontFace: "Aptos" },
                  }),
                  text("Warns about stockout risk", {
                    width: fill,
                    height: hug,
                    style: { fontSize: 24, color: colors.sky, fontFace: "Aptos" },
                  }),
                  text("Suggests next planner actions", {
                    width: fill,
                    height: hug,
                    style: { fontSize: 24, color: colors.sky, fontFace: "Aptos" },
                  }),
                ],
              ),
            ),
            column(
              { width: grow(0.8), height: fill, gap: 18 },
              [
                metricCard("Services", "9", colors.blue),
                metricCard("ML Models", "3", colors.cyan),
                metricCard("Agent Roles", "4", colors.amber),
              ],
            ),
          ],
        ),
        addFooter("Retail demand forecasting project presentation", 1),
      ],
    ),
  );
}

// Slide 2
{
  const slide = deck.slides.add();
  slideBase(
    slide,
    column(
      { width: fill, height: fill, padding: { x: 92, y: 76 }, gap: 30 },
      [
        titleBlock(
          "Problem Statement",
          "Retailers often lose revenue because they cannot estimate demand at the right time.",
        ),
        grid(
          {
            width: fill,
            height: fixed(680),
            columns: [fr(1), fr(1), fr(1)],
            rows: [fr(1)],
            columnGap: 22,
          },
          [
            bulletCard("Business Problems", [
              "Stockouts happen when demand increases suddenly.",
              "Extra inventory increases storage and wastage cost.",
              "Manual planning is slow and error-prone.",
            ]),
            bulletCard("Technical Problems", [
              "Sales data is spread across different services.",
              "Predictions are not always available in real time.",
              "Normal dashboards do not explain what action to take.",
            ]),
            bulletCard("Project Need", [
              "Forecast demand quickly.",
              "Warn about stock risk early.",
              "Give simple next actions for retail planners.",
            ], colors.mint),
          ],
        ),
        addFooter("Slide explains why the project is needed", 2),
      ],
    ),
  );
}

// Slide 3
{
  const slide = deck.slides.add();
  slideBase(
    slide,
    column(
      { width: fill, height: fill, padding: { x: 92, y: 76 }, gap: 28 },
      [
        titleBlock(
          "Objective and Scope",
          "The project focuses on short-term demand forecasting with a simple retail planning workflow.",
        ),
        row(
          { width: fill, height: fixed(700), gap: 24 },
          [
            bulletCard("Main Objective", [
              "Build a Docker-based retail analytics platform.",
              "Forecast product demand using ML.",
              "Check anomaly and stockout conditions.",
              "Support planners with easy recommendations.",
            ], colors.white),
            bulletCard("Scope of the Project", [
              "Uses synthetic retail scenarios for live demo.",
              "Works with product, store, sales, price, and stock data.",
              "Runs multiple containerized services together.",
              "Can be extended with real ERP or POS data later.",
            ], colors.white),
          ],
        ),
        addFooter("Objective and scope kept simple for viva explanation", 3),
      ],
    ),
  );
}

// Slide 4
{
  const slide = deck.slides.add();
  slideBase(
    slide,
    column(
      { width: fill, height: fill, padding: { x: 92, y: 72 }, gap: 20 },
      [
        titleBlock(
          "System Architecture",
          "The project is built as Docker microservices so every stage is separate and easy to explain.",
        ),
        grid(
          {
            width: fill,
            height: fixed(600),
            columns: [fr(1), fr(1), fr(1), fr(1), fr(1)],
            rows: [auto, auto, auto],
            columnGap: 18,
            rowGap: 18,
          },
          [
            panel({ width: fill, height: fixed(104), padding: 18, borderRadius: 20, fill: colors.white, stroke: colors.border, columnSpan: 5 },
              text("Dashboard -> Ingestion -> Preprocessing -> Router", {
                width: fill,
                height: hug,
                style: { fontSize: 28, bold: true, color: colors.navy, align: "center", fontFace: "Aptos Display" },
              })),
            panel({ width: fill, height: fixed(136), padding: 18, borderRadius: 20, fill: colors.white, stroke: colors.border },
              text("Demand Forecast Model", { width: fill, height: hug, style: { fontSize: 24, bold: true, color: colors.ink, align: "center", fontFace: "Aptos Display" } })),
            panel({ width: fill, height: fixed(136), padding: 18, borderRadius: 20, fill: colors.white, stroke: colors.border },
              text("Demand Anomaly Model", { width: fill, height: hug, style: { fontSize: 24, bold: true, color: colors.ink, align: "center", fontFace: "Aptos Display" } })),
            panel({ width: fill, height: fixed(136), padding: 18, borderRadius: 20, fill: colors.white, stroke: colors.border },
              text("Stockout Risk Model", { width: fill, height: hug, style: { fontSize: 24, bold: true, color: colors.ink, align: "center", fontFace: "Aptos Display" } })),
            panel({ width: fill, height: fixed(136), padding: 18, borderRadius: 20, fill: colors.mint, stroke: colors.border, columnSpan: 2 },
              text("Decision Hub + Agent Orchestrator", { width: fill, height: hug, style: { fontSize: 26, bold: true, color: colors.navy, align: "center", fontFace: "Aptos Display" } })),
            panel({ width: fill, height: fixed(188), padding: 20, borderRadius: 22, fill: colors.white, stroke: colors.border, columnSpan: 5 },
              column({ width: fill, height: fill, gap: 18 }, [
                text("Simple explanation", { width: fill, height: hug, style: { fontSize: 26, bold: true, color: colors.blue, fontFace: "Aptos Display" } }),
                text("1. Sales data enters and features are prepared.", { width: fill, height: hug, style: { fontSize: 20, color: colors.slate, fontFace: "Aptos" } }),
                text("2. ML models predict demand, anomaly, and stock risk.", { width: fill, height: hug, style: { fontSize: 20, color: colors.slate, fontFace: "Aptos" } }),
                text("3. Agentic AI turns the outputs into one planner action.", { width: fill, height: hug, style: { fontSize: 20, color: colors.slate, fontFace: "Aptos" } }),
              ])),
          ],
        ),
        addFooter("Architecture slide for explaining service flow", 4),
      ],
    ),
  );
}

// Slide 5
{
  const slide = deck.slides.add();
  slideBase(
    slide,
    column(
      { width: fill, height: fill, padding: { x: 92, y: 76 }, gap: 28 },
      [
        titleBlock(
          "Dataset and Input Features",
          "The demo uses synthetic retail sales data that behaves like real planning data.",
        ),
        row(
          { width: fill, height: fixed(700), gap: 22 },
          [
            bulletCard("Input Fields", [
              "Product ID and Store ID",
              "Base price and discount percent",
              "Inventory units available",
              "Prior day and prior week sales",
              "Promotion flag and holiday flag",
              "Footfall index and lead time",
            ]),
            bulletCard("Engineered Features", [
              "Effective price",
              "Daily and weekly sales velocity",
              "Stock cover days",
              "Demand pressure",
              "Promotion lift",
              "Replenishment gap",
            ]),
          ],
        ),
        addFooter("Dataset explanation without technical overload", 5),
      ],
    ),
  );
}

// Slide 6
{
  const slide = deck.slides.add();
  slideBase(
    slide,
    column(
      { width: fill, height: fill, padding: { x: 92, y: 72 }, gap: 24 },
      [
        titleBlock(
          "Models Used in the Project",
          "Different ML models are used for different retail planning tasks.",
        ),
        chart({
          name: "models-chart",
          width: fill,
          height: fixed(420),
          chartType: "bar",
          config: {
            title: "Model importance in the planning workflow",
            categories: ["Demand forecast", "Stockout risk", "Demand anomaly"],
            series: [
              {
                name: "Contribution",
                values: [90, 82, 68],
              },
            ],
          },
        }),
        grid(
          {
            width: fill,
            height: fixed(250),
            columns: [fr(1), fr(1), fr(1)],
            rows: [fr(1)],
            columnGap: 20,
          },
          [
            bulletCard("Random Forest Regressor", [
              "Used for short-term demand prediction.",
              "Outputs expected units per day.",
            ]),
            bulletCard("Logistic Regression", [
              "Used for stockout risk classification.",
              "Outputs low, medium, or urgent risk behavior.",
            ]),
            bulletCard("Isolation Forest", [
              "Used to detect unusual sales patterns.",
              "Helps identify abnormal spikes or drops.",
            ]),
          ],
        ),
        addFooter("Models slide kept simple for easy presentation", 6),
      ],
    ),
  );
}

// Slide 7
{
  const slide = deck.slides.add();
  slideBase(
    slide,
    column(
      { width: fill, height: fill, padding: { x: 92, y: 74 }, gap: 18 },
      [
        titleBlock(
          "Agentic AI Layer",
          "Agentic AI is used to convert model outputs into explainable retail actions.",
        ),
        row(
          { width: fill, height: fixed(300), gap: 18 },
          [
            metricCard("Demand Sensing Agent", "Checks forecast strength", colors.blue),
            metricCard("Inventory Guardian Agent", "Checks stock cover", colors.coral),
            metricCard("Merchandising Agent", "Checks promotion behavior", colors.cyan),
            metricCard("Supervisor Agent", "Combines final plan", colors.amber),
          ],
        ),
        bulletCard("How Agentic AI Works", [
          "Each specialist agent reads the ML outputs.",
          "Each agent gives its own conclusion and action.",
          "The supervisor agent combines all suggestions.",
          "The dashboard displays an easy final plan for planners.",
        ], colors.white),
        addFooter("Agentic AI layer explained in non-technical language", 7),
      ],
    ),
  );
}

// Slide 8
{
  const slide = deck.slides.add();
  slideBase(
    slide,
    column(
      { width: fill, height: fill, padding: { x: 92, y: 74 }, gap: 24 },
      [
        titleBlock(
          "Demo Scenarios",
          "Four ready-made scenarios help demonstrate the project during viva or live demo.",
        ),
        row(
          { width: fill, height: fixed(210), gap: 18 },
          [
            metricCard("Steady baseline", "52 units/day", colors.blue),
            metricCard("Promo surge", "126 units/day", colors.cyan),
            metricCard("Festival peak", "164 units/day", colors.amber),
            metricCard("Inventory crunch", "78 units/day", colors.coral),
          ],
        ),
        grid(
          {
            width: fill,
            height: fixed(230),
            columns: [fr(1), fr(1)],
            rows: [fr(1), fr(1)],
            columnGap: 18,
            rowGap: 18,
          },
          [
            bulletCard("Steady Baseline", ["Normal weekday demand and healthy inventory."]),
            bulletCard("Promo Surge", ["Promotion creates a fast increase in demand."]),
            bulletCard("Festival Peak", ["Holiday traffic pushes demand to a high level."]),
            bulletCard("Inventory Crunch", ["Stock is low even though sales are still active."]),
          ],
        ),
        addFooter("Scenario slide supports live demonstration", 8),
      ],
    ),
  );
}

// Slide 9
{
  const slide = deck.slides.add();
  slideBase(
    slide,
    column(
      { width: fill, height: fill, padding: { x: 92, y: 74 }, gap: 24 },
      [
        titleBlock(
          "Outputs and Business Benefits",
          "The system gives both prediction results and practical retail benefits.",
        ),
        row(
          { width: fill, height: fixed(290), gap: 22 },
          [
            metricCard("Forecast Output", "Units/day", colors.blue),
            metricCard("Risk Output", "Stockout score", colors.coral),
            metricCard("Agent Output", "Planner next actions", colors.cyan),
            metricCard("Deployment", "Docker containers", colors.amber),
          ],
        ),
        row(
          { width: fill, height: fixed(320), gap: 22 },
          [
            bulletCard("System Outputs", [
              "Demand forecast",
              "Anomaly alert",
              "Stockout risk",
              "Agent action plan",
            ]),
            bulletCard("Business Benefits", [
              "Better inventory planning",
              "Reduced stockout loss",
              "Improved promotion control",
              "Easy decision support for planners",
            ], colors.mint),
          ],
        ),
        addFooter("Slide connects technical output to business value", 9),
      ],
    ),
  );
}

// Slide 10
{
  const slide = deck.slides.add();
  slideBase(
    slide,
    column(
      { width: fill, height: fill, padding: { x: 92, y: 74 }, gap: 28 },
      [
        titleBlock(
          "Conclusion and Future Scope",
          "RetailPulse ML is a simple but industry-oriented project that combines ML, Docker, and agentic AI.",
        ),
        row(
          { width: fill, height: fixed(610), gap: 22 },
          [
            bulletCard("Conclusion", [
              "The project predicts demand in an easy-to-understand way.",
              "It separates services using Docker.",
              "It adds an agentic layer for decision support.",
              "It is suitable for academic demo and industry explanation.",
            ]),
            bulletCard("Future Scope", [
              "Connect with real retail or ERP data.",
              "Add a database and login system.",
              "Use real LLM agents for smarter planning.",
              "Deploy to cloud for multi-store use.",
            ], colors.white),
          ],
        ),
        text("Thank You", {
          name: "thanks",
          width: fill,
          height: hug,
          style: { fontSize: 36, bold: true, color: colors.blue, align: "center", fontFace: "Aptos Display" },
        }),
        addFooter("Final slide for closing the presentation", 10),
      ],
    ),
  );
}

const pptxBlob = await PresentationFile.exportPptx(deck);
const pptxPath = path.join(outputDir, "RetailPulse_ML_Presentation.pptx");
await pptxBlob.save(pptxPath);

const slideCount = deck.slides.count;

for (let index = 0; index < slideCount; index += 1) {
  const slide = deck.slides.getItem(index);
  const pngBlob = await slide.export();
  const previewPath = path.join(previewDir, `slide-${String(index + 1).padStart(2, "0")}.png`);
  await fs.writeFile(previewPath, Buffer.from(await pngBlob.bytes()));
}

console.log(JSON.stringify({ pptxPath, previewDir, slideCount }, null, 2));
