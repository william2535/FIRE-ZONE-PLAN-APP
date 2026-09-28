// Follow the visible Menu control before using a collapsed header in UI regressions.
exports.openHeader=async page=>{
 const toggle=page.locator('#topCollapseBtn');
 if(await toggle.isVisible()&&await toggle.getAttribute('aria-expanded')==='false')await toggle.click();
};
