const fs = require('fs');
const path = require('path');

console.log('--- FluxWarden Frontend Smoke Tests ---');

// 1. Verify dist files exist
const distHtml = path.join(__dirname, 'dist', 'index.html');
if (!fs.existsSync(distHtml)) {
  console.error('FAIL: dist/index.html not found');
  process.exit(1);
}
console.log('PASS: dist/index.html generated successfully.');

const content = fs.readFileSync(distHtml, 'utf8');
if (!content.includes('FLUXWARDEN') && !content.includes('FluxWarden')) {
  console.error('FAIL: Brand metadata missing from built HTML');
  process.exit(1);
}
console.log('PASS: Metadata and brand verified in index.html.');

// 2. Check components source files existence
const requiredComponents = [
  'src/app/App.tsx',
  'src/components/Navbar.tsx',
  'src/components/BackgroundCanvas.tsx',
  'src/components/ApprovalModal.tsx',
  'src/components/CommandPalette.tsx',
  'src/features/LandingPage.tsx',
  'src/features/CommandCenter.tsx',
  'src/features/AgentStatusPanel.tsx',
  'src/features/ExecutionTimeline.tsx',
  'src/features/ServiceTopology.tsx',
  'src/features/LiveMetrics.tsx',
  'src/features/ChatMission.tsx',
  'src/features/AgentTerminal.tsx',
  'src/features/FinalResolutionCard.tsx',
  'src/features/ChaosLab.tsx',
  'src/features/ArchitecturePage.tsx',
  'src/features/JudgeScorecard.tsx',
  'src/features/OperationalMemoryView.tsx',
  'src/features/IncidentDetail.tsx',
  'src/features/SettingsView.tsx',
  'src/hooks/useAgentEvents.ts',
  'src/hooks/useKeyboardShortcuts.ts',
  'src/lib/utils.ts',
  'src/lib/constants.ts',
  'src/animations/framerAnimations.ts',
  'src/visualizations/TopologyCanvas.tsx',
  'src/visualizations/MetricsChartCanvas.tsx'
];

for (const comp of requiredComponents) {
  const fullPath = path.join(__dirname, comp);
  if (!fs.existsSync(fullPath)) {
    console.error(`FAIL: Missing required component: ${comp}`);
    process.exit(1);
  }
}
console.log(`PASS: All ${requiredComponents.length} React components verified in source tree.`);

console.log('--- All Frontend Smoke Tests Passed 100% ---');
