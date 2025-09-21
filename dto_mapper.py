import json
from typing import Dict, Any, List, Optional
from datetime import datetime, date

class DTOMapper:
    def __init__(self):
        # Load master data mappings
        with open("complete_master_data_mappings_csv_only.json", "r", encoding="utf-8") as f:
            self.master_data = json.load(f)["master_data_mappings"]
    
    def map_to_dto(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Map extracted resume data to the required DTO format
        """
        try:
            # Create base DTO structure
            dto = self._create_base_dto()
            
            # Map personal information
            if "personal_info" in extracted_data:
                dto["empApplnPersonalDataDTO"] = self._map_personal_data(extracted_data["personal_info"])
                dto["addressDetailDTO"] = self._map_address_data(extracted_data["personal_info"])
            
            # Map education
            if "education" in extracted_data:
                dto["educationalDetailDTO"] = self._map_education_data(extracted_data["education"])
            
            # Map work experience
            if "work_experience" in extracted_data:
                dto["professionalExperienceDTO"] = self._map_work_experience(extracted_data["work_experience"])
            
            # Map research experience
            if "research_experience" in extracted_data:
                dto["researchDetailDTO"] = self._map_research_experience(extracted_data["research_experience"])
            
            # Map additional information
            if "additional_informations" in extracted_data:
                dto["additionalInformations"] = self._map_additional_info(extracted_data["additional_informations"])
            
            return dto
            
        except Exception as e:
            raise Exception(f"Error mapping to DTO: {str(e)}")
    
    def _create_base_dto(self) -> Dict[str, Any]:
        """Create base DTO structure"""
        return {
            "empApplnEntriesId": 0,
            "saveMode": "save draft",
            "applicationNo": None,
            "empApplicationRegistrationId": None,
            "isAvailableForTheInterview": None,
            "empApplnInterviewSchedulesId": None,
            "interviewRound": None,
            "isAcceptOffer": None,
            "reportingDate": None,
            "joiningDate": None,
            "jobDetailDTO": {
                "empApplnEntriesId": 0,
                "postAppliedFor": "1",
                "subjectCategoryIds": [[]],
                "specializationIds": None,
                "empApplnSubjectCategoryDTO": [],
                "preferredLocationIds": [],
                "empDTO": None,
                "empJobDetails": None,
                "erpRoomEmpMappingDTO": None,
                "empGuestContractDetailsDTO": None,
                "subjectCategory": None,
                "subjectSpecialization": None,
                "empApplnCampusPrefDTOList": None
            },
            "empApplnPersonalDataDTO": {},
            "addressDetailDTO": {},
            "educationalDetailDTO": {},
            "professionalExperienceDTO": {},
            "researchDetailDTO": {
                "isResearchExperience": "No",
                "inflibnetVidwanNo": None,
                "scopusId": None,
                "hIndex": None,
                "researchEntries": {
                    "empApplnAddtnlInfoEntriesId": None,
                    "isResearchExperience": None,
                    "researchEntriesHeadings": None,
                    "entriesId": None,
                    "parameterId": None,
                    "addtnlInfoValue": None
                },
                "isInterviewedBefore": "No",
                "interviewedBeforeDepartment": None,
                "interviewedBeforeYear": None,
                "interviewedBeforeApplicationNo": None,
                "interviewedBeforeSubject": None,
                "vacancyInformationId": "5",
                "aboutVacancyOthers": None,
                "otherInformation": None,
                "orcidId": None,
                "hindex": None
            },
            "additionalPersonalDataDTO": None,
            "empJobDetailsDTO": None,
            "empApplnNonAvailabilityDTO": None,
            "jobCategoryDTO": None,
            "empGratuityNomineesDTO": None,
            "empPfNomineesDTO": None,
            "regretLetterfileUploadDownloadDTO": None,
            "familyDetailsAddtnlList": None,
            "dependentDetailsAddtnlList": None,
            "additionalInformations": None,
            "empApplnSubjectCategory": None,
            "empApplnSubjectCategorySpecialization": None,
            "locationPref": None,
            "academic": False,
            "maritalStatusDTO": None,
            "submissionDate": None,
            "identityRow": None,
            "campusPreference": None,
            "applicantWorkFlowStatusCode": None,
            "applicationWorkFlowStatusCode": None,
            "empAppliedEmployeCategory": None,
            "majorAchievements": None,
            "offerLetterfileUploadDownloadDTO": None
        }
    
    def _map_personal_data(self, personal_info: Dict[str, Any]) -> Dict[str, Any]:
        """Map personal information to DTO"""
        return {
            "empApplnPersonalDataId": 0,
            "empApplnEntriesId": 0,
            "applicantName": personal_info.get("name", ""),
            "genderId": self._find_master_id("gender", personal_info.get("gender", "")),
            "fatherName": None,  # Not typically in resumes
            "motherName": None,  # Not typically in resumes
            "dateOfBirth": self._format_date(personal_info.get("date_of_birth")),
            "emailId": personal_info.get("email", ""),
            "mobileNoCountryCode": "+91",  # Default for India
            "mobileNo": personal_info.get("phone", ""),
            "alternateNo": None,
            "aadharNo": personal_info.get("aadhar_no"),
            "maritalStatusId": self._find_master_id("marital_status", personal_info.get("marital_status", "")),
            "nationalityId": self._find_master_id("country", personal_info.get("nationality", "India")),
            "passportNo": personal_info.get("passport_no"),
            "religionId": self._find_master_id("religion", personal_info.get("religion", "")),
            "isMinority": "No",  # Default
            "reservationCategoryId": "3",  # Default
            "bloodGroupId": self._find_master_id("blood_group", personal_info.get("blood_group", "")),
            "isDifferentlyAbled": "No",  # Default
            "differentlyAbledId": None,
            "differentlyAbledDetails": None,
            "currentAddressLine1": None,
            "currentAddressLine2": None,
            "currentCountryId": None,
            "currentStateId": None,
            "currentStateOthers": None,
            "currentCityId": None,
            "currentCityOthers": None,
            "currentPincode": None,
            "isPermanentEqualsCurrent": None,
            "permanentAddressLine1": None,
            "permanentAddressLine2": None,
            "permanentCountryId": None,
            "permanentStateId": None,
            "permanentStateOthers": None,
            "permanentCityId": None,
            "permanentCityOthers": None,
            "permanentPincode": None,
            "profilePhotoUrl": None,
            "isUanNo": None,
            "uanNo": None,
            "highestQualificationLevel": None,
            "originalFileName": None,
            "uniqueFileName": None,
            "newFile": False,
            "processCode": None,
            "actualPath": None,
            "tempPath": None,
            "orcidNo": None,
            "vidwanNo": None,
            "scopusNo": None,
            "resumeUploadDTO": None,
            "resumeUrl": None,
            "hindexNo": None
        }
    
    def _map_address_data(self, personal_info: Dict[str, Any]) -> Dict[str, Any]:
        """Map address information to DTO"""
        address = personal_info.get("address", "")
        return {
            "empApplnPersonalDataId": 0,
            "empApplnEntriesId": 0,
            "applicantName": None,
            "genderId": None,
            "fatherName": None,
            "motherName": None,
            "dateOfBirth": None,
            "emailId": None,
            "mobileNoCountryCode": None,
            "mobileNo": None,
            "alternateNo": None,
            "aadharNo": None,
            "maritalStatusId": None,
            "nationalityId": None,
            "passportNo": None,
            "religionId": None,
            "isMinority": None,
            "reservationCategoryId": None,
            "bloodGroupId": None,
            "isDifferentlyAbled": None,
            "differentlyAbledId": None,
            "differentlyAbledDetails": None,
            "currentAddressLine1": address,
            "currentAddressLine2": None,
            "currentCountryId": "1",  # Default to India
            "currentStateId": None,
            "currentStateOthers": None,
            "currentCityId": None,
            "currentCityOthers": None,
            "currentPincode": None,
            "isPermanentEqualsCurrent": "Yes",
            "permanentAddressLine1": address,
            "permanentAddressLine2": None,
            "permanentCountryId": "1",  # Default to India
            "permanentStateId": None,
            "permanentStateOthers": None,
            "permanentCityId": None,
            "permanentCityOthers": None,
            "permanentPincode": None,
            "profilePhotoUrl": None,
            "isUanNo": None,
            "uanNo": None,
            "highestQualificationLevel": None,
            "originalFileName": None,
            "uniqueFileName": None,
            "newFile": None,
            "processCode": None,
            "actualPath": None,
            "tempPath": None,
            "orcidNo": None,
            "vidwanNo": None,
            "scopusNo": None,
            "resumeUploadDTO": None,
            "resumeUrl": None,
            "hindexNo": None
        }
    
    def _map_education_data(self, education: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Map education data to DTO"""
        if not education:
            return {
                "highestQualificationLevelId": None,
                "highestQualificationAlbum": None,
                "highestQualification": None,
                "qualificationLevelsList": [],
                "eligibilityTestList": None,
                "otherQualificationLevelsList": None,
                "empEducationalDetailsMap": {},
                "eligibilityTestDetails": None,
                "empEducationalDetailsDTOS": None,
                "studentEducationalDetailsDTOList": None
            }
        
        # Find highest qualification
        highest_level = self._find_highest_qualification(education)
        
        qualification_levels = []
        for i, edu in enumerate(education):
            qualification_levels.append({
                "empApplnEducationalDetailsId": 0,
                "empApplnEntriesId": 0,
                "qualificationName": None,
                "qualificationLevelId": self._map_qualification_level(edu.get("qualification_level", "")),
                "qualificationOthers": None,
                "currentStatus": self._get_current_status(edu.get("current_status", edu.get("year_of_completion", ""))),
                "course": self._normalize_course_name(edu.get("course", ""), edu.get("qualification_level", "")),
                "specialization": edu.get("specialization", ""),
                "yearOfCompletion": self._extract_year_from_completion(edu.get("year_of_completion", "")),
                "gradeOrPercentage": edu.get("grade_or_percentage", ""),
                "institute": edu.get("institute", ""),
                "boardOrUniversity": edu.get("board_or_university", ""),
                "documentList": [],
                "qualificationLevelName": None,
                "countryId": self._find_master_id("country", edu.get("country", "India")),
                "stateId": self._find_master_id("state", edu.get("state", "")),
                "stateOther": None,
                "erpInstitute": None,
                "erpBoardOrUniversity": None,
                "qualificationLevelCode": None,
                "countryName": None,
                "stateName": None
            })
        
        return {
            "highestQualificationLevelId": highest_level,
            "highestQualificationAlbum": None,
            "highestQualification": None,
            "qualificationLevelsList": qualification_levels,
            "eligibilityTestList": None,
            "otherQualificationLevelsList": None,
            "empEducationalDetailsMap": {},
            "eligibilityTestDetails": None,
            "empEducationalDetailsDTOS": None,
            "studentEducationalDetailsDTOList": None
        }
    
    def _map_work_experience(self, work_exp: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Map work experience data to DTO"""
        if not work_exp:
            return {
                "isCurrentlyWorking": "No",
                "currentExperience": None,
                "professionalExperienceList": None,
                "totalPreviousExperienceYears": "0",
                "totalPreviousExperienceMonths": "0",
                "totalPartTimePreviousExperienceYears": "0",
                "totalPartTimePreviousExperienceMonths": "0",
                "recognisedExpYears": None,
                "recognisedExpMonths": None,
                "fullTimeYears": None,
                "fullTimeMonths": None,
                "partTimeYears": None,
                "partTimeMonths": None,
                "majorAchievements": None,
                "expectedSalary": None,
                "experienceInformation": None,
                "majorAchievementsList": None
            }
        
        # Find current experience (most recent or marked as current)
        current_exp = None
        for exp in work_exp:
            to_date = str(exp.get("to_date", "")).lower()
            if to_date in ["present", "current", ""] or "present" in to_date:
                current_exp = exp
                break
        
        if not current_exp and work_exp:
            # If no current experience found, check if the most recent one is ongoing
            # by checking if it's PhD or research work
            for exp in work_exp:
                designation = str(exp.get("designation", "")).lower()
                if any(term in designation for term in ["phd", "ph.d", "research", "student", "candidate"]):
                    current_exp = exp
                    break
            
            # If still no current exp, take the first one
            if not current_exp:
                current_exp = work_exp[0]
        
        # Calculate total experience (excluding current experience)
        total_years, total_months = self._calculate_previous_experience(work_exp, current_exp)
        
        current_experience_dto = None
        if current_exp:
            current_experience_dto = {
                "empApplnWorkExperienceId": 0,
                "empApplnEntriesId": 0,
                "workExperienceTypeId": "2",  # Default
                "functionalAreaId": "13",  # Default
                "functionalAreaOthers": None,
                "employmentType": current_exp.get("employment_type", "fulltime"),
                "designation": current_exp.get("designation", ""),
                "years": str(self._calculate_years_from_dates(current_exp.get("from_date"), current_exp.get("to_date"))),
                "months": str(self._calculate_months_from_dates(current_exp.get("from_date"), current_exp.get("to_date"))),
                "noticePeriod": str(current_exp.get("notice_period", 30)),
                "currentSalary": str(current_exp.get("current_salary", 0)),
                "institution": current_exp.get("company", ""),
                "experienceDocumentList": [],
                "functionalArea": None,
                "fromDate": self._parse_date_array(current_exp.get("from_date")),
                "toDate": self._parse_date_array(current_exp.get("to_date"), is_current=True if current_exp.get("to_date", "").lower() in ["present", "current"] else False),
                "isPartTime": None,
                "isCurrentExperience": None
            }
        
        return {
            "isCurrentlyWorking": "Yes" if current_exp else "No",
            "currentExperience": current_experience_dto,
            "professionalExperienceList": None,
            "totalPreviousExperienceYears": str(total_years),
            "totalPreviousExperienceMonths": str(total_months),
            "totalPartTimePreviousExperienceYears": "0",
            "totalPartTimePreviousExperienceMonths": "0",
            "recognisedExpYears": None,
            "recognisedExpMonths": None,
            "fullTimeYears": None,
            "fullTimeMonths": None,
            "partTimeYears": None,
            "partTimeMonths": None,
            "majorAchievements": None,
            "expectedSalary": None,
            "experienceInformation": None,
            "majorAchievementsList": None
        }
    
    def _map_research_experience(self, research_info: Dict[str, Any]) -> Dict[str, Any]:
        """Map research experience to DTO"""
        has_research = research_info.get("has_research", False)
        
        return {
            "isResearchExperience": "Yes" if has_research else "No",
            "inflibnetVidwanNo": None,
            "scopusId": None,
            "hIndex": None,
            "researchEntries": {
                "empApplnAddtnlInfoEntriesId": None,
                "isResearchExperience": "Yes" if has_research else "No",
                "researchEntriesHeadings": None,
                "entriesId": None,
                "parameterId": None,
                "addtnlInfoValue": None
            },
            "isInterviewedBefore": "No",
            "interviewedBeforeDepartment": None,
            "interviewedBeforeYear": None,
            "interviewedBeforeApplicationNo": None,
            "interviewedBeforeSubject": None,
            "vacancyInformationId": "5",
            "aboutVacancyOthers": None,
            "otherInformation": None,
            "orcidId": None,
            "hindex": None
        }
    
    def _map_additional_info(self, additional_info: Dict[str, Any]) -> Dict[str, Any]:
        """Map additional information to DTO"""
        def safe_get(key, default=None):
            value = additional_info.get(key, default)
            # Return null if empty list, empty string, or None
            if value is None or value == "" or (isinstance(value, list) and len(value) == 0):
                return None
            return value
        
        def normalize_awards(awards):
            """Normalize award names to be more concise"""
            if not awards or not isinstance(awards, list):
                return awards
            
            normalized = []
            for award in awards:
                if isinstance(award, str) and len(award) > 80:
                    # If award name is very long, try to shorten it
                    if "award" in award.lower():
                        # Extract the main award name and keep the description in parentheses
                        parts = award.split("award", 1)
                        if len(parts) > 1:
                            main_part = parts[0].strip() + " Award"
                            desc_part = parts[1].strip()
                            # Clean up the description part
                            if desc_part and not desc_part.startswith("("):
                                # If description doesn't start with parentheses, add them
                                normalized.append(f"{main_part} ({desc_part})")
                            else:
                                normalized.append(f"{main_part} {desc_part}")
                        else:
                            normalized.append(award)
                    else:
                        # Just truncate if too long
                        normalized.append(award[:80] + "..." if len(award) > 80 else award)
                else:
                    normalized.append(award)
            
            return normalized
        
        return {
            "profile_summary": additional_info.get("profile_summary") or None,
            "skills": safe_get("skills", []),
            "awards": normalize_awards(safe_get("awards")),
            "publications": safe_get("publications"),
            "conferences": safe_get("conferences"),
            "collaborators": safe_get("collaborators"),
            "languages": safe_get("languages"),
            "certifications": safe_get("certifications"),
            "volunteer_work": safe_get("volunteer_work")
        }
    
    def _find_master_id(self, category: str, value: str) -> str:
        """Find master data ID for a given category and value"""
        if not value or category not in self.master_data:
            return "1"  # Default ID
        
        # Convert value to string and handle None/empty values
        value_str = str(value).strip() if value is not None else ""
        if not value_str:
            return "1"  # Default ID
        
        values = self.master_data[category].get("values", [])
        for item in values:
            item_name = str(item.get("name", "")).strip()
            if value_str.lower() in item_name.lower():
                return str(item.get("id", 1))
        
        return "1"  # Default ID
    
    def _map_qualification_level(self, level: str) -> str:
        """Map qualification level to ID"""
        if not level:
            return "3"  # Default to UG
            
        level_str = str(level).strip().lower()
        level_mapping = {
            "class 10": "1",
            "class 12": "2", 
            "ug": "3",
            "pg": "4",
            "phd": "5",
            "ph.d": "5",
            "doctorate": "5",
            "master": "4",
            "msc": "4",
            "m.sc": "4",
            "bachelor": "3",
            "bsc": "3",
            "b.sc": "3"
        }
        
        for key, value in level_mapping.items():
            if key in level_str:
                return value
        
        return "3"  # Default to UG
    
    def _find_highest_qualification(self, education: List[Dict[str, Any]]) -> str:
        """Find highest qualification level ID"""
        levels = []
        for edu in education:
            level = str(edu.get("qualification_level", "")).strip().lower()
            if "phd" in level or "ph.d" in level or "doctorate" in level:
                levels.append(5)
            elif "pg" in level or "post graduate" in level or "master" in level or "msc" in level or "m.sc" in level:
                levels.append(4)
            elif "ug" in level or "undergraduate" in level or "bachelor" in level or "bsc" in level or "b.sc" in level:
                levels.append(3)
            elif "class 12" in level or "12th" in level:
                levels.append(2)
            elif "class 10" in level or "10th" in level:
                levels.append(1)
        
        return str(max(levels)) if levels else "3"
    
    def _calculate_total_experience(self, work_exp: List[Dict[str, Any]]) -> tuple:
        """Calculate total years and months of experience"""
        total_years = 0
        total_months = 0
        
        for exp in work_exp:
            try:
                # Try to get years and months from the exp data
                years = int(exp.get("years", 0)) if exp.get("years") is not None else 0
                months = int(exp.get("months", 0)) if exp.get("months") is not None else 0
                
                # If years/months not provided, try to calculate from dates
                if years == 0 and months == 0:
                    from_date = exp.get("from_date", "")
                    to_date = exp.get("to_date", "")
                    
                    if from_date and to_date:
                        years, months = self._calculate_experience_from_dates(from_date, to_date)
                
                total_years += years
                total_months += months
            except (ValueError, TypeError):
                # Skip invalid values
                continue
        
        # Convert months to years
        total_years += total_months // 12
        total_months = total_months % 12
        
        return total_years, total_months
    
    def _calculate_experience_from_dates(self, from_date: str, to_date: str) -> tuple:
        """Calculate years and months from date strings"""
        try:
            from datetime import datetime
            
            # Parse from_date
            from_dt = None
            for fmt in ["%Y-%m-%d", "%d-%m-%Y", "%m/%d/%Y", "%d/%m/%Y"]:
                try:
                    from_dt = datetime.strptime(from_date, fmt)
                    break
                except ValueError:
                    continue
            
            # Parse to_date
            to_dt = None
            if to_date.lower() in ["present", "current"]:
                to_dt = datetime.now()
            else:
                for fmt in ["%Y-%m-%d", "%d-%m-%Y", "%m/%d/%Y", "%d/%m/%Y"]:
                    try:
                        to_dt = datetime.strptime(to_date, fmt)
                        break
                    except ValueError:
                        continue
            
            if from_dt and to_dt:
                # Calculate difference
                delta = to_dt - from_dt
                years = delta.days // 365
                months = (delta.days % 365) // 30
                return years, months
                
        except Exception:
            pass
        
        return 0, 0
    
    def _calculate_previous_experience(self, work_exp: List[Dict[str, Any]], current_exp: Dict[str, Any]) -> tuple:
        """Calculate total previous experience (excluding current experience)"""
        total_years = 0
        total_months = 0
        
        for exp in work_exp:
            # Skip if this is the current experience
            if exp == current_exp:
                continue
                
            try:
                # Try to get years and months from the exp data
                years = int(exp.get("years", 0)) if exp.get("years") is not None else 0
                months = int(exp.get("months", 0)) if exp.get("months") is not None else 0
                
                # If years/months not provided, try to calculate from dates
                if years == 0 and months == 0:
                    from_date = exp.get("from_date", "")
                    to_date = exp.get("to_date", "")
                    
                    if from_date and to_date:
                        years, months = self._calculate_experience_from_dates(from_date, to_date)
                
                total_years += years
                total_months += months
            except (ValueError, TypeError):
                # Skip invalid values
                continue
        
        # Convert months to years
        total_years += total_months // 12
        total_months = total_months % 12
        
        return total_years, total_months
    
    def _calculate_years_from_dates(self, from_date: str, to_date: str) -> int:
        """Calculate years from date strings"""
        try:
            from datetime import datetime
            
            # Parse from_date
            from_dt = None
            for fmt in ["%Y-%m-%d", "%d-%m-%Y", "%m/%d/%Y", "%d/%m/%Y"]:
                try:
                    from_dt = datetime.strptime(from_date, fmt)
                    break
                except ValueError:
                    continue
            
            # Parse to_date
            to_dt = None
            if to_date and to_date.lower() in ["present", "current"]:
                to_dt = datetime.now()
            elif to_date:
                for fmt in ["%Y-%m-%d", "%d-%m-%Y", "%m/%d/%Y", "%d/%m/%Y"]:
                    try:
                        to_dt = datetime.strptime(to_date, fmt)
                        break
                    except ValueError:
                        continue
            
            if from_dt and to_dt:
                # Calculate difference
                delta = to_dt - from_dt
                years = delta.days // 365
                return years
                
        except Exception:
            pass
        
        return 0
    
    def _calculate_months_from_dates(self, from_date: str, to_date: str) -> int:
        """Calculate months from date strings"""
        try:
            from datetime import datetime
            
            # Parse from_date
            from_dt = None
            for fmt in ["%Y-%m-%d", "%d-%m-%Y", "%m/%d/%Y", "%d/%m/%Y"]:
                try:
                    from_dt = datetime.strptime(from_date, fmt)
                    break
                except ValueError:
                    continue
            
            # Parse to_date
            to_dt = None
            if to_date and to_date.lower() in ["present", "current"]:
                to_dt = datetime.now()
            elif to_date:
                for fmt in ["%Y-%m-%d", "%d-%m-%Y", "%m/%d/%Y", "%d/%m/%Y"]:
                    try:
                        to_dt = datetime.strptime(to_date, fmt)
                        break
                    except ValueError:
                        continue
            
            if from_dt and to_dt:
                # Calculate difference
                delta = to_dt - from_dt
                total_months = (to_dt.year - from_dt.year) * 12 + (to_dt.month - from_dt.month)
                # Subtract the years already counted
                years = delta.days // 365
                months = total_months - (years * 12)
                return max(0, months)
                
        except Exception:
            pass
        
        return 0
    
    def _format_date(self, date_str: str) -> str:
        """Format date string to ISO format"""
        if not date_str:
            return None
        
        try:
            # Try different date formats
            for fmt in ["%Y-%m-%d", "%d-%m-%Y", "%m/%d/%Y", "%d/%m/%Y"]:
                try:
                    parsed_date = datetime.strptime(date_str, fmt).date()
                    return parsed_date.isoformat() + "T18:30:00.000Z"
                except ValueError:
                    continue
        except:
            pass
        
        return None
    
    def _extract_year_from_completion(self, completion_str: str) -> str:
        """Extract year from completion string, handling cases like 'Thesis submitted'"""
        if not completion_str:
            return ""
        
        completion_str = str(completion_str).strip()
        
        # If it's already a year (4 digits)
        if completion_str.isdigit() and len(completion_str) == 4:
            return completion_str
        
        # Handle date ranges like "2016-2018" - extract the END year
        import re
        range_match = re.search(r'(\d{4})-(\d{4})', completion_str)
        if range_match:
            return range_match.group(2)  # Return the end year
        
        # Extract year from text like "Thesis submitted 2024" or "2024"
        year_match = re.search(r'\b(20\d{2}|19\d{2})\b', completion_str)
        if year_match:
            return year_match.group(1)
        
        # If no year found and it's ongoing, return empty string (let currentStatus handle it)
        if any(phrase in completion_str.lower() for phrase in ["thesis submitted", "ongoing", "pursuing", "current"]):
            return ""
        
        # If no year found, return empty string
        return ""
    
    def _get_current_status(self, status_str: str) -> str:
        """Get current status from completion string"""
        if not status_str:
            return None
        
        status_str = str(status_str).strip().lower()
        
        # Check if it contains status indicators
        if any(phrase in status_str for phrase in ["thesis submitted", "ongoing", "pursuing", "current"]):
            return status_str.title()
        
        return None
    
    def _parse_date_array(self, date_str: str, is_current: bool = False) -> List[int]:
        """Parse date string to [year, month, day] array"""
        if not date_str or date_str.lower() in ["present", "current"]:
            return None  # Return null for ongoing positions
        
        try:
            for fmt in ["%Y-%m-%d", "%d-%m-%Y", "%m/%d/%Y", "%d/%m/%Y"]:
                try:
                    parsed_date = datetime.strptime(date_str, fmt).date()
                    return [parsed_date.year, parsed_date.month, parsed_date.day]
                except ValueError:
                    continue
        except:
            pass
        
        # Try to extract year from string
        import re
        year_match = re.search(r'\b(20\d{2}|19\d{2})\b', str(date_str))
        if year_match:
            year = int(year_match.group(1))
            return [year, 1, 1]  # Default to January 1st
        
        return None  # Return null if date cannot be parsed
    
    def _normalize_course_name(self, course: str, qualification_level: str) -> str:
        """Normalize course names to proper degree names"""
        if not course:
            return ""
        
        course = str(course).strip()
        qualification_level = str(qualification_level).lower()
        
        # If course looks like a designation, convert to proper degree name
        if any(term in course.lower() for term in ["researcher", "scholar", "candidate", "student"]):
            if "phd" in qualification_level or "ph.d" in qualification_level:
                return "Ph.D."
            elif "pg" in qualification_level or "master" in qualification_level:
                return "M.Sc."
            elif "ug" in qualification_level or "bachelor" in qualification_level:
                return "B.Sc."
            elif "class 12" in qualification_level:
                return "Class 12"
            elif "class 10" in qualification_level:
                return "Class 10"
        
        # If course looks like a university name (contains "university", "college", "institute")
        if any(term in course.lower() for term in ["university", "college", "institute", "school", "mumbai", "delhi", "iit", "mit", "harvard", "stanford"]):
            if "phd" in qualification_level or "ph.d" in qualification_level:
                return "Ph.D."
            elif "pg" in qualification_level or "master" in qualification_level or "msc" in qualification_level:
                return "M.Sc."
            elif "ug" in qualification_level or "bachelor" in qualification_level or "bsc" in qualification_level:
                return "B.Sc."
            elif "class 12" in qualification_level:
                return "Class 12"
            elif "class 10" in qualification_level:
                return "Class 10"
        
        # If course already looks like a degree name, return as is
        if any(term in course.upper() for term in ["PH.D", "M.SC", "B.SC", "B.TECH", "M.TECH", "MBA", "CLASS"]):
            return course
        
        # Default mapping based on qualification level
        if "phd" in qualification_level or "ph.d" in qualification_level:
            return "Ph.D."
        elif "pg" in qualification_level or "master" in qualification_level or "msc" in qualification_level:
            return "M.Sc."
        elif "ug" in qualification_level or "bachelor" in qualification_level or "bsc" in qualification_level:
            return "B.Sc."
        elif "class 12" in qualification_level:
            return "Class 12"
        elif "class 10" in qualification_level:
            return "Class 10"
        
        return course  # Return original if no mapping found
