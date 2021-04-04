INSERT INTO Region (region_name) 
SELECT DISTINCT(test_tb.regname)
FROM test_tb
WHERE test_tb.regname IS NOT NULL
ON CONFLICT (region_name) DO NOTHING;

INSERT INTO EO_types (eo_type_name) 
SELECT DISTINCT(test_tb.eotypename)
FROM test_tb
WHERE test_tb.eotypename IS NOT NULL
ON CONFLICT (eo_type_name) DO NOTHING;

INSERT INTO EO_parents (parent_name) 
SELECT DISTINCT(test_tb.eoparent)
FROM test_tb
WHERE test_tb.eoparent IS NOT NULL
ON CONFLICT (parent_name) DO NOTHING;

INSERT INTO Class_profiles (profile_name) 
SELECT DISTINCT(test_tb.classprofilename)
FROM test_tb
WHERE test_tb.classprofilename IS NOT NULL
ON CONFLICT (profile_name) DO NOTHING;

INSERT INTO Participant_status (status_name) 
SELECT DISTINCT(test_tb.regtypename)
FROM test_tb
WHERE test_tb.regtypename IS NOT NULL
ON CONFLICT (status_name) DO NOTHING;

INSERT INTO Languages (lang_name) 
SELECT DISTINCT(test_tb.classlangname)
FROM test_tb
WHERE test_tb.classlangname IS NOT NULL
ON CONFLICT (lang_name) DO NOTHING;

INSERT INTO Ter_type_name (type_name) 
SELECT DISTINCT(test_tb.tertypename)
FROM test_tb
WHERE test_tb.tertypename IS NOT NULL
ON CONFLICT (type_name) DO NOTHING;
-- /*==============================================================*/
-- /* Table: Subjects INSERT                                          */
-- /*==============================================================*/
INSERT INTO Subjects (subject_name) 
	SELECT DISTINCT(test_tb.ukrtest)
	FROM test_tb
	WHERE test_tb.ukrtest IS NOT NULL

	UNION

	SELECT DISTINCT(test_tb.histtest)
	FROM test_tb
	WHERE test_tb.histtest IS NOT NULL

	UNION

	SELECT DISTINCT(test_tb.mathtest)
	FROM test_tb
	WHERE test_tb.mathtest IS NOT NULL

	UNION

	SELECT DISTINCT(test_tb.phystest)
	FROM test_tb
	WHERE test_tb.phystest IS NOT NULL

	UNION

	SELECT DISTINCT(test_tb.chemtest)
	FROM test_tb
	WHERE test_tb.chemtest IS NOT NULL

	UNION

	SELECT DISTINCT(test_tb.biotest)
	FROM test_tb
	WHERE test_tb.biotest IS NOT NULL

	UNION

	SELECT DISTINCT(test_tb.geotest)
	FROM test_tb
	WHERE test_tb.geotest IS NOT NULL

	UNION

	SELECT DISTINCT(test_tb.engtest)
	FROM test_tb
	WHERE test_tb.engtest IS NOT NULL

	UNION

	SELECT DISTINCT(test_tb.fratest)
	FROM test_tb
	WHERE test_tb.fratest IS NOT NULL

	UNION

	SELECT DISTINCT(test_tb.deutest)
	FROM test_tb
	WHERE test_tb.deutest IS NOT NULL

	UNION

	SELECT DISTINCT(test_tb.spatest)
	FROM test_tb
	WHERE test_tb.spatest IS NOT NULL;

-- /*==============================================================*/
-- /* Table: DISTRICT                                          */
-- /*==============================================================*/

INSERT INTO district (region_id, district_name) 
SELECT DISTINCT region.region_id, area
FROM
	(SELECT DISTINCT test_tb.regname as reg, test_tb.areaname as area
	FROM test_tb
	WHERE test_tb.areaname IS NOT NULL

	UNION

	SELECT DISTINCT test_tb.eoregname, test_tb.eoareaname
	FROM test_tb
	WHERE test_tb.eoareaname IS NOT NULL) as reg_area, region
where reg_area.reg = region_name
ON CONFLICT (region_id, district_name) DO NOTHING;

-- /*==============================================================*/
-- /* Table:                                           */
-- /*==============================================================*/
INSERT INTO locality (district_id, type_id, locality_name)
SELECT 
	res.district_id,
	res.type_id,
    res.ter 
    
   FROM(
  SELECT 
    with_reg_id.ter,
    with_reg_id.area,
    with_reg_id.region_id,
	DISTRICT.district_id,
    with_reg_id.type_id
   FROM(
	   SELECT creg_area.reg,
    creg_area.area,
    creg_area.ter,
    creg_area.tertype,
    region.region_id,
    ter_type_name.type_id
   FROM (SELECT reg_ar_ter.reg, reg_ar_ter.area, reg_ar_ter.ter,tt.tertype
	from (
	SELECT DISTINCT reg, area, ter
	FROM
	(SELECT DISTINCT test_tb.regname as reg, test_tb.areaname as area, test_tb.tername as ter
	FROM test_tb

	UNION

	SELECT DISTINCT test_tb.eoregname, test_tb.eoareaname, test_tb.eotername
	 
	FROM test_tb
	 
	UNION SELECT DISTINCT test_tb.ukrptregname , test_tb.ukrptareaname , test_tb.ukrpttername FROM test_tb
	UNION SELECT DISTINCT test_tb.histptregname , test_tb.histptareaname , test_tb.histpttername FROM test_tb
	UNION SELECT DISTINCT test_tb.mathptregname , test_tb.mathptareaname , test_tb.mathpttername FROM test_tb
	UNION SELECT DISTINCT test_tb.physptregname , test_tb.physptareaname , test_tb.physpttername FROM test_tb
	UNION SELECT DISTINCT test_tb.chemptregname , test_tb.chemptareaname , test_tb.chempttername FROM test_tb
	UNION SELECT DISTINCT test_tb.bioptregname , test_tb.bioptareaname , test_tb.biopttername FROM test_tb
	UNION SELECT DISTINCT test_tb.geoptregname , test_tb.geoptareaname , test_tb.geopttername FROM test_tb
	UNION SELECT DISTINCT test_tb.engptregname , test_tb.engptareaname , test_tb.engpttername FROM test_tb
	UNION SELECT DISTINCT test_tb.fraptregname , test_tb.fraptareaname , test_tb.frapttername FROM test_tb
	UNION SELECT DISTINCT test_tb.deuptregname , test_tb.deuptareaname , test_tb.deupttername FROM test_tb
	UNION SELECT DISTINCT test_tb.spaptregname , test_tb.spaptareaname , test_tb.spapttername FROM test_tb

	) as reg_area
where ter is not NULL) as reg_ar_ter
left outer join (
SELECT DISTINCT test_tb.regname as reg, test_tb.areaname as area, test_tb.tername as ter,test_tb.tertypename as tertype 
	FROM test_tb
) as tt on(
reg_ar_ter.reg =tt.reg and
reg_ar_ter.area=tt.area and
reg_ar_ter.ter=tt.ter 
))creg_area
     LEFT JOIN region ON (creg_area.reg = region.region_name)
	 LEFT JOIN ter_type_name ON (creg_area.tertype = ter_type_name.type_name)) with_reg_id
	 LEFT OUTER JOIN DISTRICT ON((with_reg_id.REGION_ID = DISTRICT.REGION_ID) AND (with_reg_id.area = DISTRICT.district_name))) as res
ON CONFLICT (district_id, locality_name) DO NOTHING;
------------------------------------------------------------------------------------------------------
CREATE OR REPLACE VIEW place_view
AS
SELECT locality.locality_id,
   locality.locality_name,
   district.district_name,
   region.region_name
  FROM ((locality
    LEFT JOIN district ON ((locality.district_id = district.district_id)))
    LEFT JOIN region ON ((district.region_id = region.region_id)));
------------------------------------------------------------------------------------------------------
INSERT INTO educational_institution (institution_name, locality_id, eo_type_id, parent_id)
SELECT DISTINCT t2.eoname, place_view.locality_id, t2.eo_type_id, t2.parent_id
from(
SELECT DISTINCT test_tb.eoname, test_tb.eoregname, test_tb.eoareaname, test_tb.eotername, eo_types.eo_type_id, eo_parents.parent_id
FROM test_tb
left outer join eo_parents on (test_tb.eoparent = eo_parents.parent_name)
left outer join eo_types on (test_tb.eotypename = eo_types.eo_type_name)
UNION
SELECT DISTINCT pt_name, reg, area, ter, cast(pt_type as integer), cast(pt_parent as integer)
from(
SELECT DISTINCT test_tb.ukrptname as pt_name, test_tb.ukrptregname as reg, test_tb.ukrptareaname as area, test_tb.ukrpttername as ter, NULL as pt_type, NULL as pt_parent FROM test_tb
UNION SELECT DISTINCT test_tb.histptname , test_tb.histptregname , test_tb.histptareaname , test_tb.histpttername, NULL, NULL FROM test_tb
UNION SELECT DISTINCT test_tb.mathptname , test_tb.mathptregname , test_tb.mathptareaname , test_tb.mathpttername, NULL, NULL FROM test_tb
UNION SELECT DISTINCT test_tb.physptname , test_tb.physptregname , test_tb.physptareaname , test_tb.physpttername, NULL, NULL FROM test_tb
UNION SELECT DISTINCT test_tb.chemptname , test_tb.chemptregname , test_tb.chemptareaname , test_tb.chempttername, NULL, NULL FROM test_tb
UNION SELECT DISTINCT test_tb.bioptname , test_tb.bioptregname , test_tb.bioptareaname , test_tb.biopttername, NULL, NULL FROM test_tb
UNION SELECT DISTINCT test_tb.geoptname , test_tb.geoptregname , test_tb.geoptareaname , test_tb.geopttername, NULL, NULL FROM test_tb
UNION SELECT DISTINCT test_tb.engptname , test_tb.engptregname , test_tb.engptareaname , test_tb.engpttername, NULL, NULL FROM test_tb
UNION SELECT DISTINCT test_tb.fraptname , test_tb.fraptregname , test_tb.fraptareaname , test_tb.frapttername, NULL, NULL FROM test_tb
UNION SELECT DISTINCT test_tb.deuptname , test_tb.deuptregname , test_tb.deuptareaname , test_tb.deupttername, NULL, NULL FROM test_tb
UNION SELECT DISTINCT test_tb.spaptname , test_tb.spaptregname , test_tb.spaptareaname , test_tb.spapttername, NULL, NULL FROM test_tb
) t1
WHERE NOT EXISTS(
SELECT DISTINCT test_tb.eoname, test_tb.eoregname, test_tb.eoareaname, test_tb.eotername, eo_types.eo_type_id, eo_parents.parent_id
FROM test_tb
left outer join eo_parents on (test_tb.eoparent = eo_parents.parent_name)
left outer join eo_types on (test_tb.eotypename = eo_types.eo_type_name)
WHERE test_tb.eoname = t1.pt_name and
	test_tb.eoregname = t1.reg and
	test_tb.eoareaname = t1.area  and
	test_tb.eotername = t1.ter 
) ) as t2
left outer join place_view on
(t2.eoregname = place_view.region_name and
t2.eoareaname = place_view.district_name and
t2.eotername = place_view.locality_name)
where t2.eoname is not null
ON CONFLICT (institution_name, locality_id, eo_type_id, parent_id) DO NOTHING;

------------------------------------------------------------------------------------------------------

CREATE OR REPLACE VIEW eo_view
AS
SELECT DISTINCT min(educational_institution.institution_id), educational_institution.institution_name, place_view.region_name, place_view.district_name, place_view.locality_name
from educational_institution
left join place_view on(
educational_institution.locality_id = place_view.locality_id)
group by educational_institution.institution_name, place_view.region_name, place_view.district_name, place_view.locality_name;
------------------------------------------------------------------------------------------------------


INSERT INTO participants (out_id, birth, sex_type_name, locality_id, status_id, profile_id, lang_id, institution_id) 
select DISTINCT
test_tb.outid,  
test_tb.birth,
test_tb.sextypename, 

place_view.locality_id,
participant_status.status_id,
class_profiles.profile_id,
languages.lang_id,
educational_institution.institution_id

from test_tb
left join place_view on(
test_tb.regname = place_view.region_name and
test_tb.areaname = place_view.district_name and
test_tb.tername = place_view.locality_name )
left join participant_status on(
test_tb.regtypename = participant_status.status_name)
left join languages on(
test_tb.classlangname = languages.lang_name)
left join class_profiles on(
test_tb.classprofilename = class_profiles.profile_name)
left join eo_types on(
test_tb.eotypename = eo_types.eo_type_name)	
left join educational_institution on(
place_view.locality_id = educational_institution.locality_id and
test_tb.eoname = educational_institution.institution_name and
eo_types.eo_type_id = educational_institution.eo_type_id
) 
where test_tb.outid IS NOT NULL
ON CONFLICT (out_id) DO NOTHING;


INSERT INTO passing_exam (out_id, subject_id, institution_id, lang_id, test_status, dpa_level, ball100, ball12, ball, adapt_scale, zno_year)  
select  
test_tb.outid,
subjects.subject_id,
eo_view.institution_id,
NULL as lang_id,
test_tb.ukrteststatus,
NULL as dpa_level,
test_tb.ukrball100,
test_tb.ukrball12,
test_tb.ukrball,
test_tb.ukradaptscale as adapt_scale,
test_tb.zno_year

from test_tb
left join subjects on (test_tb.ukrtest = subjects.subject_name)
left join eo_view on 
(test_tb.ukrptname = eo_view.institution_name and
 test_tb.ukrptregname = eo_view.region_name and
 test_tb.ukrptareaname = eo_view.district_name and
 test_tb.ukrpttername = eo_view.locality_name 
)
where test_tb.ukrtest is not NULL;

INSERT INTO passing_exam (out_id, subject_id, institution_id, lang_id, test_status, dpa_level, ball100, ball12, ball, adapt_scale, zno_year) 
 select  
test_tb.outid,
subjects.subject_id,
eo_view.institution_id,
languages.lang_id,
test_tb.histteststatus,
NULL as dpa_level,
test_tb.histball100,
test_tb.histball12,
test_tb.histball,
NULL as adapt_scale,
test_tb.zno_year

from test_tb
left join subjects on (test_tb.histtest = subjects.subject_name)
left join languages on (test_tb.histlang = languages.lang_name)
left join eo_view on 
(test_tb.histptname = eo_view.institution_name and
 test_tb.histptregname = eo_view.region_name and
 test_tb.histptareaname = eo_view.district_name and
 test_tb.histpttername = eo_view.locality_name 
)
where test_tb.histtest is not NULL;

INSERT INTO passing_exam (out_id, subject_id, institution_id, lang_id, test_status, dpa_level, ball100, ball12, ball, adapt_scale, zno_year) 
 select  
test_tb.outid,
subjects.subject_id,
eo_view.institution_id,
languages.lang_id,
test_tb.mathteststatus,
NULL as dpa_level,
test_tb.mathball100,
test_tb.mathball12,
test_tb.mathball,
NULL as adapt_scale,
test_tb.zno_year

from test_tb
left join subjects on (test_tb.mathtest = subjects.subject_name)
left join languages on (test_tb.mathlang = languages.lang_name)
left join eo_view on 
(test_tb.mathptname = eo_view.institution_name and
 test_tb.mathptregname = eo_view.region_name and
 test_tb.mathptareaname = eo_view.district_name and
 test_tb.mathpttername = eo_view.locality_name 
)
where test_tb.mathtest is not NULL;

INSERT INTO passing_exam (out_id, subject_id, institution_id, lang_id, test_status, dpa_level, ball100, ball12, ball, adapt_scale, zno_year) 
 select  
test_tb.outid,
subjects.subject_id,
eo_view.institution_id,
languages.lang_id,
test_tb.physteststatus,
NULL as dpa_level,
test_tb.physball100,
test_tb.physball12,
test_tb.physball,
NULL as adapt_scale,
test_tb.zno_year

from test_tb
left join subjects on (test_tb.phystest = subjects.subject_name)
left join languages on (test_tb.physlang = languages.lang_name)
left join eo_view on 
(test_tb.physptname = eo_view.institution_name and
 test_tb.physptregname = eo_view.region_name and
 test_tb.physptareaname = eo_view.district_name and
 test_tb.physpttername = eo_view.locality_name 
)
where test_tb.phystest is not NULL;

INSERT INTO passing_exam (out_id, subject_id, institution_id, lang_id, test_status, dpa_level, ball100, ball12, ball, adapt_scale, zno_year) 
 select  
test_tb.outid,
subjects.subject_id,
eo_view.institution_id,
languages.lang_id,
test_tb.chemteststatus,
NULL as dpa_level,
test_tb.chemball100,
test_tb.chemball12,
test_tb.chemball,
NULL as adapt_scale,
test_tb.zno_year

from test_tb
left join subjects on (test_tb.chemtest = subjects.subject_name)
left join languages on (test_tb.chemlang = languages.lang_name)
left join eo_view on 
(test_tb.chemptname = eo_view.institution_name and
 test_tb.chemptregname = eo_view.region_name and
 test_tb.chemptareaname = eo_view.district_name and
 test_tb.chempttername = eo_view.locality_name 
)
where test_tb.chemtest is not NULL;

INSERT INTO passing_exam (out_id, subject_id, institution_id, lang_id, test_status, dpa_level, ball100, ball12, ball, adapt_scale, zno_year)  
select  
test_tb.outid,
subjects.subject_id,
eo_view.institution_id,
languages.lang_id,
test_tb.bioteststatus,
NULL as dpa_level,
test_tb.bioball100,
test_tb.bioball12,
test_tb.bioball,
NULL as adapt_scale,
test_tb.zno_year

from test_tb
left join subjects on (test_tb.biotest = subjects.subject_name)
left join languages on (test_tb.biolang = languages.lang_name)
left join eo_view on 
(test_tb.bioptname = eo_view.institution_name and
 test_tb.bioptregname = eo_view.region_name and
 test_tb.bioptareaname = eo_view.district_name and
 test_tb.biopttername = eo_view.locality_name 
)
where test_tb.biotest is not NULL;

INSERT INTO passing_exam (out_id, subject_id, institution_id, lang_id, test_status, dpa_level, ball100, ball12, ball, adapt_scale, zno_year) 
 select  
test_tb.outid,
subjects.subject_id,
eo_view.institution_id,
languages.lang_id,
test_tb.geoteststatus,
NULL as dpa_level,
test_tb.geoball100,
test_tb.geoball12,
test_tb.geoball,
NULL as adapt_scale,
test_tb.zno_year

from test_tb
left join subjects on (test_tb.geotest = subjects.subject_name)
left join languages on (test_tb.geolang = languages.lang_name)
left join eo_view on 
(test_tb.geoptname = eo_view.institution_name and
 test_tb.geoptregname = eo_view.region_name and
 test_tb.geoptareaname = eo_view.district_name and
 test_tb.geopttername = eo_view.locality_name 
)
where test_tb.geotest is not NULL;

INSERT INTO passing_exam (out_id, subject_id, institution_id, lang_id, test_status, dpa_level, ball100, ball12, ball, adapt_scale, zno_year)  
select  
test_tb.outid,
subjects.subject_id,
eo_view.institution_id,
NULL as lang_id,
test_tb.engteststatus,
test_tb.engdpalevel as dpa_level,
test_tb.engball100,
test_tb.engball12,
test_tb.engball,
NULL as adapt_scale,
test_tb.zno_year

from test_tb
left join subjects on (test_tb.engtest = subjects.subject_name)
left join eo_view on 
(test_tb.engptname = eo_view.institution_name and
 test_tb.engptregname = eo_view.region_name and
 test_tb.engptareaname = eo_view.district_name and
 test_tb.engpttername = eo_view.locality_name 
)
where test_tb.engtest is not NULL;

INSERT INTO passing_exam (out_id, subject_id, institution_id, lang_id, test_status, dpa_level, ball100, ball12, ball, adapt_scale, zno_year)  
select  
test_tb.outid,
subjects.subject_id,
eo_view.institution_id,
NULL as lang_id,
test_tb.frateststatus,
test_tb.fradpalevel as dpa_level,
test_tb.fraball100,
test_tb.fraball12,
test_tb.fraball,
NULL as adapt_scale,
test_tb.zno_year

from test_tb
left join subjects on (test_tb.fratest = subjects.subject_name)
left join eo_view on 
(test_tb.fraptname = eo_view.institution_name and
 test_tb.fraptregname = eo_view.region_name and
 test_tb.fraptareaname = eo_view.district_name and
 test_tb.frapttername = eo_view.locality_name 
)
where test_tb.fratest is not NULL;

INSERT INTO passing_exam (out_id, subject_id, institution_id, lang_id, test_status, dpa_level, ball100, ball12, ball, adapt_scale, zno_year)  
select  
test_tb.outid,
subjects.subject_id,
eo_view.institution_id,
NULL as lang_id,
test_tb.deuteststatus,
test_tb.deudpalevel as dpa_level,
test_tb.deuball100,
test_tb.deuball12,
test_tb.deuball,
NULL as adapt_scale,
test_tb.zno_year

from test_tb
left join subjects on (test_tb.deutest = subjects.subject_name)
left join eo_view on 
(test_tb.deuptname = eo_view.institution_name and
 test_tb.deuptregname = eo_view.region_name and
 test_tb.deuptareaname = eo_view.district_name and
 test_tb.deupttername = eo_view.locality_name 
)
where test_tb.deutest is not NULL;

INSERT INTO passing_exam (out_id, subject_id, institution_id, lang_id, test_status, dpa_level, ball100, ball12, ball, adapt_scale, zno_year) 
 select  
test_tb.outid,
subjects.subject_id,
eo_view.institution_id,
NULL as lang_id,
test_tb.spateststatus,
test_tb.spadpalevel as dpa_level,
test_tb.spaball100,
test_tb.spaball12,
test_tb.spaball,
NULL as adapt_scale,
test_tb.zno_year

from test_tb
left join subjects on (test_tb.spatest = subjects.subject_name)
left join eo_view on 
(test_tb.spaptname = eo_view.institution_name and
 test_tb.spaptregname = eo_view.region_name and
 test_tb.spaptareaname = eo_view.district_name and
 test_tb.spapttername = eo_view.locality_name 
)
where test_tb.spatest is not NULL;

