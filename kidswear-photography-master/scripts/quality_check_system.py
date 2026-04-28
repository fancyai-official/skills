#!/usr/bin/env python3
"""
Kidswear Editorial Generation Quality Check System
Automatically verifies whether all user-requested optimizations have been correctly executed
"""

def quality_check_system(prompt_text, generation_params, model_race, shot_number):
    """
    Quality Check System - Verifies if the prompt meets all user optimization requirements
    
    Args:
        prompt_text: Full prompt text for generating the image
        generation_params: Generation parameters dictionary (including img_urls, ratio, etc.)
        model_race: Model type ("asian" or "european")
                    Note: Asian black hair check has been removed, this parameter is currently only used to identify Shot type in log prints,
                    and does not affect any check results. Kept only for interface backward compatibility.
        shot_number: Shot number (1-5)
    
    Returns:
        dict: {
            "passed": bool,  # Whether it passed the quality check
            "errors": list,  # Failed check items
            "warnings": list  # Warning items
        }
    """
    errors = []
    warnings = []
    
    print(f"\n{'='*80}")
    print(f"🔍 Quality Check System - Shot {shot_number} ({model_race} model)")
    print(f"{'='*80}")
    
    # ========== Check 1: Asian model black hair (Removed) ==========
    # Hairstyle description has been removed from the 4-layer prompt structure, no longer checking for black hair requirement
    has_black_hair = None  # Fixed as None, skip this item in the report
    
    # ========== Check 2: Complete Outfit Styling (Top and Bottom) ==========
    print("\n✓ Check 2: Complete outfit styling")
    
    has_complete_outfit = "Complete Outfit" in prompt_text or "complete outfit" in prompt_text.lower()
    has_upper_body = "Upper body:" in prompt_text or "upper body" in prompt_text.lower()
    has_lower_body = "Lower body:" in prompt_text or "lower body" in prompt_text.lower()
    has_full_outfit_type = "wearing the complete outfit" in prompt_text.lower() or "garment_type: full_outfit" in prompt_text.lower() or "garment_type: dress" in prompt_text.lower()
    
    if not has_complete_outfit:
        warnings.append("⚠️  Missing 'Complete Outfit' marker")
        print("   ⚠️  Did not find 'Complete Outfit' marker")
    else:
        print("   ✅ Contains 'Complete Outfit'")
    
    if has_full_outfit_type:
        print("   ✅ Detected full outfit/dress type, no need to separately check Upper/Lower body")
    elif not (has_upper_body and has_lower_body):
        errors.append("❌ CRITICAL: Garment description missing Upper body/Lower body layers - must explicitly state top and bottom")
        print(f"   ❌ Upper body: {has_upper_body}, Lower body: {has_lower_body}")
    else:
        print("   ✅ Contains Upper/Lower body descriptions")
    
    # ========== Check 3: Shot 2 Prohibits Jumping Action ==========
    if shot_number == 2:
        print("\n✓ Check 3: Shot 2 prohibits jumping")
        
        has_feet_planted = "feet firmly planted" in prompt_text.lower() or "feet planted" in prompt_text.lower()
        has_not_jumping = "NOT jumping" in prompt_text or "not jumping" in prompt_text.lower()
        has_grounded = "grounded" in prompt_text.lower()
        
        # Check if it contains jump-related words (these should be prohibited, excluding cases immediately following NOT)
        import re as _re
        has_forbidden = bool(_re.search(
            r'(?<![Nn][Oo][Tt] )\b(jump(?:ing)?|hop(?:ping)?|airborne|feet leaving|in the air)\b',
            prompt_text
        ))
        
        if not has_feet_planted:
            errors.append("❌ CRITICAL: Shot 2 missing 'feet firmly planted' - must emphasize feet on the ground")
            print("   ❌ Did not find 'feet firmly planted'")
        else:
            print("   ✅ Contains 'feet firmly planted'")
        
        if not has_not_jumping:
            errors.append("❌ CRITICAL: Shot 2 missing 'NOT jumping' marker - must explicitly prohibit jumping")
            print("   ❌ Did not find 'NOT jumping'")
        else:
            print("   ✅ Contains 'NOT jumping'")
        
        if has_forbidden:
            errors.append("❌ CRITICAL: Shot 2 prompt contains jump-related vocabulary - strictly prohibited")
            print("   ❌ Found prohibited jumping vocabulary")
        else:
            print("   ✅ Did not find prohibited vocabulary")
    
    # ========== Check 4: Model Consistency (Shot 2-5 must pass model_reference) ==========
    if shot_number >= 2:
        print(f"\n✓ Check 4: Shot {shot_number} model consistency")
        
        img_urls = generation_params.get("img_urls", [])
        has_model_reference = len(img_urls) >= 2
        
        if not has_model_reference:
            errors.append(f"❌ CRITICAL: Shot {shot_number} img_urls must contain 2 URLs (garment + model_reference)")
            print(f"   ❌ img_urls length: {len(img_urls)} (should be >= 2)")
        else:
            print(f"   ✅ img_urls contains {len(img_urls)} URLs (garment + model_reference)")
        
        # Check if the prompt mentions using the same model
        has_same_model = "Same" in prompt_text and "model" in prompt_text.lower()
        if not has_same_model:
            warnings.append(f"⚠️  Shot {shot_number} prompt does not explicitly state using the same model")
            print("   ⚠️  Did not find 'Same...model' marker")
        else:
            print("   ✅ Prompt contains same model marker")
    
    # ========== Check 5: Scene Layer Description (Removed) ==========
    # Layer 5 (Scene Environment) has been removed from the 4-layer prompt structure, no longer requires Foreground/Mid-ground/Background layered descriptions
    scene_layers = [True, True, True]  # Fixed to pass, to avoid missing scene_layers key in report
    
    # ========== Check 6: Commercial Editorial Standard (Precise Body Description) ==========
    print("\n✓ Check 6: Commercial editorial standard")
    
    # Check if it contains precise descriptions for multiple body parts
    # ⚠️ Note: SKILL.md's 4-layer structure does not mandate these English section tags, so this item is changed to a warning instead of an error
    body_parts = ["Feet:", "Knees:", "Hips:", "Torso:", "Arms:", "Hands:", "Head:", "Eyes:", "Expression:"]
    found_parts = [part for part in body_parts if part in prompt_text]
    
    if len(found_parts) < 5:
        warnings.append(f"⚠️  Pose description has few English body tags (found {len(found_parts)}), recommended to add more to improve precision (not mandatory)")
        print(f"   ⚠️  Found {len(found_parts)} body part tags (not mandatory, for hint purposes): {', '.join(found_parts) if found_parts else 'None'}")
    else:
        print(f"   ✅ Found precise descriptions for {len(found_parts)} body parts")
    
    # Check for NOT markers (distinguishing commercial vs. daily)
    not_markers = ["NOT casual", "NOT everyday", "NOT snapshot", "NOT jumping", "NOT blurry"]
    found_markers = [marker for marker in not_markers if marker in prompt_text]
    
    if len(found_markers) < 1:
        warnings.append("⚠️  Missing NOT markers distinguishing commercial vs. daily")
        print("   ⚠️  Did not find NOT markers (commercial vs. daily distinction)")
    else:
        print(f"   ✅ Found {len(found_markers)} NOT markers")
    
    # ========== Check 7: Generation Parameter Validation ==========
    print("\n✓ Check 7: Generation parameters")
    
    ratio = generation_params.get("ratio", "")
    if ratio != "3:4":
        errors.append(f"❌ CRITICAL: Image ratio error - current: {ratio}, should be: 3:4")
        print(f"   ❌ Ratio: {ratio} (should be 3:4)")
    else:
        print(f"   ✅ Ratio correct: {ratio}")
    
    image_size = generation_params.get("image_size", "")
    if image_size != "4K":
        warnings.append(f"⚠️  Image size is not 4K - current: {image_size}")
        print(f"   ⚠️  Size: {image_size} (recommended 4K)")
    else:
        print(f"   ✅ Size: {image_size}")
    
    # ========== Summary ==========
    print(f"\n{'='*80}")
    passed = len(errors) == 0
    
    if passed:
        print("✅ Quality check passed! All key check items meet requirements")
    else:
        print(f"❌ Quality check failed! Found {len(errors)} critical errors")
    
    if warnings:
        print(f"⚠️  Found {len(warnings)} warnings")
    
    print(f"{'='*80}\n")
    
    return {
        "passed": passed,
        "errors": errors,
        "warnings": warnings,
        "checks": {
            "complete_outfit": has_complete_outfit,
            "no_jumping": has_not_jumping if shot_number == 2 else None,
            "model_consistency": has_model_reference if shot_number >= 2 else None,
            "scene_layers": len([l for l in scene_layers if l]) == 3,
            "body_precision": len(found_parts) >= 5,
            "commercial_standard": len(found_markers) >= 1
        }
    }


def enforce_quality_check(prompt_text, generation_params, model_race, shot_number):
    """
    Enforce quality check - if it does not pass, throw an exception and terminate generation
    
    Usage:
        enforce_quality_check(shot1_prompt, {...}, "asian", 1)
    """
    result = quality_check_system(prompt_text, generation_params, model_race, shot_number)
    
    if not result["passed"]:
        error_msg = "\n".join([
            "🚨 Quality check failed! The following issues must be fixed:",
            "",
            *result["errors"],
            "",
            "Please check the prompt construction logic to ensure all user optimization requirements are implemented."
        ])
        raise ValueError(error_msg)
    
    if result["warnings"]:
        print("⚠️  Quality check passed but with warnings:")
        for warning in result["warnings"]:
            print(f"  {warning}")
        print()
    
    return result


# ========== Quality Check Report Generator ==========
def generate_quality_report(all_results):
    """
    Generate a complete 5-image quality check report
    
    Args:
        all_results: list of quality_check_system results for Shot 1-5
    
    Returns:
        str: Formatted report text
    """
    report = ["", "="*80, "📊 Kidswear Editorial Generation Quality Check Report", "="*80, ""]
    
    total_errors = sum(len(r["errors"]) for r in all_results)
    total_warnings = sum(len(r["warnings"]) for r in all_results)
    passed_count = sum(1 for r in all_results if r["passed"])
    
    report.append(f"Overall result: {passed_count}/5 images passed quality check")
    report.append(f"Critical errors: {total_errors}")
    report.append(f"Warnings: {total_warnings}")
    report.append("")
    
    # Pass rate of each check item
    report.append("Check item pass status:")
    checks = ["complete_outfit", "no_jumping", "model_consistency",
              "body_precision", "commercial_standard"]
    check_names = {
        "complete_outfit": "Complete outfit styling",
        "no_jumping": "Shot2 prohibits jumping",
        "model_consistency": "Model consistency",
        "body_precision": "Precise body description",
        "commercial_standard": "Commercial editorial standard"
    }
    
    for check in checks:
        passed = sum(1 for r in all_results if r["checks"].get(check) is True)
        total = sum(1 for r in all_results if r["checks"].get(check) is not None)
        if total > 0:
            status = "✅" if passed == total else "❌"
            report.append(f"  {status} {check_names[check]}: {passed}/{total}")
    
    report.append("")
    report.append("="*80)
    
    if total_errors == 0:
        report.append("✅ All optimization requirements have been correctly implemented!")
    else:
        report.append("❌ Quality issues found, please fix them before re-generating!")
    
    report.append("="*80)
    report.append("")
    
    return "\n".join(report)


# ========== Usage Example ==========
if __name__ == "__main__":
    print("Kidswear Editorial Generation Quality Check System")
    print("="*80)
    print()
    print("Usage Instructions:")
    print()
    print("1. Call quality check before generating each image:")
    print()
    print("   # Shot 1")
    print("   result = quality_check_system(")
    print("       prompt_text=shot1_prompt,")
    print("       generation_params={'img_urls': [garment_url], 'ratio': '3:4', 'image_size': '4K'},")
    print("       model_race='asian',")
    print("       shot_number=1")
    print("   )")
    print()
    print("2. Or use enforce quality check (terminates if not passed):")
    print()
    print("   enforce_quality_check(shot2_prompt, {...}, 'asian', 2)")
    print()
    print("3. Generate complete report:")
    print()
    print("   all_results = [result1, result2, result3, result4, result5]")
    print("   report = generate_quality_report(all_results)")
    print("   print(report)")
    print()
    print("="*80)
