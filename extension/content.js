const POLL_INTERVAL_MS = 60 * 1000;       // Check every minute
const HEARTBEAT_MS = 15 * 60 * 1000;      // Force a snapshot every 15 minutes
const API_BASE = "http://127.0.0.1:8787";

const ENDPOINTS = {
    ingest: `${API_BASE}/ingest`,
    scoreboard: `${API_BASE}/scoreboard`
};

let lastStatsJson = null;
let lastHeartbeat = 0;

function getNextData() {
  const script = document.querySelector("#__NEXT_DATA__");

  if (!script?.textContent) {
    console.log("[MakerWorld Scoreboard] No __NEXT_DATA__ script tag found.");
    return null;
  }

  try {
    return JSON.parse(script.textContent);
  } catch (error) {
    console.error("[MakerWorld Scoreboard] Failed to parse __NEXT_DATA__.", error);
    return null;
  }
}

function extractStats() {
  const data = getNextData();
  const userInfo = data?.props?.pageProps?.userInfo;

  if (!userInfo) {
    console.log("[MakerWorld Scoreboard] No userInfo found in __NEXT_DATA__.");
    console.log("[MakerWorld Scoreboard] pageProps keys:", Object.keys(data?.props?.pageProps ?? {}));
    return null;
  }

  return {
    capturedAt: new Date().toISOString(),
    source: "makerworld-next-data-script",
    handle: "@makermatt3D",
    collects: userInfo?.collectionCount ?? null,
    downloads: userInfo?.MWCount?.myInstanceDownloadCount ?? null,
    prints: userInfo?.MWCount?.myInstancePrintCount ?? null,
    boosts: userInfo?.boostGained ?? null,
    followers: userInfo?.fanCount ?? null,
    likes: userInfo?.likeCount ?? null
  };
}

async function maybeSendStats() {
    const stats = extractStats();
    console.log(`[MakerWorld Scoreboard] Polling MakerWorld stats...`);

    if (!stats) {
      console.log(`[MakerWorld Scoreboard] Poll skipped: no stats extracted.`);
        return;
    }

    const now = Date.now();
    const json = JSON.stringify(stats);

    const statsChanged = json !== lastStatsJson;
    const heartbeatExpired = (now - lastHeartbeat) > HEARTBEAT_MS;

    if (!statsChanged && !heartbeatExpired) {
        console.log("[MakerWorld Scoreboard] No changes.");
        return;
    }

    try {
        const response = await fetch(ENDPOINTS.ingest, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: json
        });

        console.log(
            `[Scoreboard] Snapshot sent (${statsChanged ? "changed" : "heartbeat"})`
        );

        lastStatsJson = json;
        lastHeartbeat = now;

    } catch (err) {
        console.error("[MakerWorld Scoreboard] Failed to send snapshot.", err);
    }
}

setTimeout(() => {
    maybeSendStats();

    setInterval(maybeSendStats, POLL_INTERVAL_MS);
}, 3000);