
DROP VIEW if exists eo_view;
DROP VIEW if exists place_view;

alter table if exists District
   drop constraint if exists FK_DISTRICT_REFERENCE_REGION;
   
alter table if exists Locality
   drop constraint if exists FK_LOCALITY_REFERENCE_DISTRICT;
alter table if exists Locality
   drop constraint if exists FK_LOCALITY_REFERENCE_TER_TYPE; 
   
alter table if exists Participants
   drop constraint if exists FK_PARTICIP_REFERENCE_CLASS_PR;
alter table if exists Participants
   drop constraint if exists FK_PARTICIP_REFERENCE_PARTICIP;   
alter table if exists Participants
   drop constraint if exists FK_PARTICIP_REFERENCE_LANGUAGE; 
alter table if exists Participants
   drop constraint if exists FK_PARTICIP_REFERENCE_EDUCATIO;   
alter table if exists Participants
   drop constraint if exists FK_PARTICIP_REFERENCE_LOCALITY; 
   
alter table if exists Educational_institution
   drop constraint if exists FK_EDUCATIO_REFERENCE_EO_TYPES ;
alter table if exists Educational_institution
   drop constraint if exists FK_EDUCATIO_REFERENCE_EO_PAREN ;
alter table if exists Educational_institution
   drop constraint if exists FK_EDUCATIO_REFERENCE_LOCALITY  ;

alter table if exists Passing_exam
   drop constraint if exists FK_PASSING__REFERENCE_PARTICIP ;
alter table if exists Passing_exam
   drop constraint if exists FK_PASSING__REFERENCE_SUBJECTS ;
alter table if exists Passing_exam
   drop constraint if exists FK_PASSING__REFERENCE_EDUCATIO ;
alter table if exists Passing_exam
   drop constraint if exists FK_PASSING__REFERENCE_LANGUAGE ;
/*==============================================================*/
alter table if exists Class_profiles
   drop constraint if exists AK_KEY_2_CLASS_PR;

drop table if exists Class_profiles;

alter table if exists District
   drop constraint if exists AK_KEY_2_DISTRICT;

drop table if exists District;

alter table if exists EO_parents
   drop constraint if exists AK_KEY_2_EO_PAREN;

drop table if exists EO_parents;

alter table if exists EO_types
   drop constraint if exists AK_KEY_2_EO_TYPES;

drop table if exists EO_types;

alter table if exists Educational_institution
   drop constraint if exists AK_KEY_2_EDUCATIO;
   
drop table if exists Educational_institution;

alter table if exists Languages
   drop constraint if exists AK_KEY_2_LANGUAGE;

drop table if exists Languages;

alter table if exists Locality
   drop constraint if exists AK_KEY_2_LOCALITY;

drop table if exists Locality;

alter table if exists Participant_status
   drop constraint if exists AK_KEY_2_PARTICIP;

drop table if exists Participant_status;

drop table if exists Participants;

drop table if exists Passing_exam;

alter table if exists Region
   drop constraint if exists AK_KEY_2_REGION;

drop table if exists Region;

alter table if exists Subjects
   drop constraint if exists AK_KEY_2_SUBJECTS;

drop table if exists Subjects;

alter table if exists Ter_type_name
   drop constraint if exists AK_KEY_2_TER_TYPE;

drop table if exists Ter_type_name;


/*==============================================================*/
/* Table: Class_profiles                                        */
/*==============================================================*/
create table Class_profiles (
   profile_id           serial               not null,
   profile_name         TEXT                 not null,
   constraint PK_CLASS_PROFILES primary key (profile_id)
);

alter table Class_profiles
   add constraint AK_KEY_2_CLASS_PR unique (profile_name);

/*==============================================================*/
/* Table: District                                              */
/*==============================================================*/
create table District (
   district_id          serial               not null,
   region_id            integer              null,
   district_name        TEXT                 null,
   constraint PK_DISTRICT primary key (district_id)
);

alter table District
   add constraint AK_KEY_2_DISTRICT unique (region_id, district_name);

/*==============================================================*/
/* Table: EO_parents                                            */
/*==============================================================*/
create table EO_parents (
   parent_id            serial               not null,
   parent_name          TEXT                 not null,
   constraint PK_EO_PARENTS primary key (parent_id)
);

alter table EO_parents
   add constraint AK_KEY_2_EO_PAREN unique (parent_name);

/*==============================================================*/
/* Table: EO_types                                              */
/*==============================================================*/
create table EO_types (
   eo_type_id           serial               not null,
   eo_type_name         TEXT                 not null,
   constraint PK_EO_TYPES primary key (eo_type_id)
);

alter table EO_types
   add constraint AK_KEY_2_EO_TYPES unique (eo_type_name);

/*==============================================================*/
/* Table: Educational_institution                               */
/*==============================================================*/
create table Educational_institution (
   institution_id       serial               not null,
   locality_id          integer              null,
   eo_type_id           integer              null,
   parent_id            integer              null,
   institution_name     TEXT                 null,
   constraint PK_EDUCATIONAL_INSTITUTION primary key (institution_id)
);

alter table Educational_institution
   add constraint AK_KEY_2_EDUCATIO unique (locality_id, institution_name, eo_type_id, parent_id);

/*==============================================================*/
/* Table: Languages                                             */
/*==============================================================*/
create table Languages (
   lang_id              serial               not null,
   lang_name            TEXT                 not null,
   constraint PK_LANGUAGES primary key (lang_id)
);

alter table Languages
   add constraint AK_KEY_2_LANGUAGE unique (lang_name);

/*==============================================================*/
/* Table: Locality                                              */
/*==============================================================*/
create table Locality (
   locality_id          serial               not null,
   district_id          integer              null,
   type_id              integer              null,
   locality_name        TEXT                 null,
   constraint PK_LOCALITY primary key (locality_id)
);

alter table Locality
   add constraint AK_KEY_2_LOCALITY unique (district_id, locality_name);

/*==============================================================*/
/* Table: Participant_status                                    */
/*==============================================================*/
create table Participant_status (
   status_id            serial               not null,
   status_name          TEXT                 not null,
   constraint PK_PARTICIPANT_STATUS primary key (status_id)
);

alter table Participant_status
   add constraint AK_KEY_2_PARTICIP unique (status_name);

/*==============================================================*/
/* Table: Participants                                          */
/*==============================================================*/
create table Participants (
   out_id               TEXT                 not null,
   locality_id          integer              null,
   profile_id           integer              null,
   status_id            integer              null,
   lang_id              integer              null,
   institution_id       integer              null,
   birth                integer              null,
   sex_type_name        TEXT                 null,
   constraint PK_PARTICIPANTS primary key (out_id)
);

/*==============================================================*/
/* Table: Passing_exam                                          */
/*==============================================================*/
create table Passing_exam (
   zno_id               serial               not null,
   out_id               TEXT                 null,
   subject_id           integer              null,
   institution_id       integer              null,
   lang_id              integer              null,
   test_status          TEXT                 null,
   dpa_level            TEXT                 null,
   ball100              NUMERIC              null,
   ball12               integer              null,
   ball                 integer              null,
   adapt_scale          integer              null,
   zno_year             integer              not null,
   constraint PK_PASSING_EXAM primary key (zno_id)
);

/*==============================================================*/
/* Table: Region                                                */
/*==============================================================*/
create table Region (
   region_id            SERIAL               not null,
   region_name          TEXT                 not null,
   constraint PK_REGION primary key (region_id)
);

alter table Region
   add constraint AK_KEY_2_REGION unique (region_name);

/*==============================================================*/
/* Table: Subjects                                              */
/*==============================================================*/
create table Subjects (
   subject_id           serial               not null,
   subject_name         TEXT                 not null,
   constraint PK_SUBJECTS primary key (subject_id)
);

alter table Subjects
   add constraint AK_KEY_2_SUBJECTS unique (subject_name);

/*==============================================================*/
/* Table: Ter_type_name                                         */
/*==============================================================*/
create table Ter_type_name (
   type_id              serial               not null,
   type_name            TEXT                 not null,
   constraint PK_TER_TYPE_NAME primary key (type_id)
);

alter table Ter_type_name
   add constraint AK_KEY_2_TER_TYPE unique (type_name);

alter table District
   add constraint FK_DISTRICT_REFERENCE_REGION foreign key (region_id)
      references Region (region_id)
      on delete restrict on update restrict;

alter table Educational_institution
   add constraint FK_EDUCATIO_REFERENCE_EO_TYPES foreign key (eo_type_id)
      references EO_types (eo_type_id)
      on delete restrict on update restrict;

alter table Educational_institution
   add constraint FK_EDUCATIO_REFERENCE_EO_PAREN foreign key (parent_id)
      references EO_parents (parent_id)
      on delete restrict on update restrict;

alter table Educational_institution
   add constraint FK_EDUCATIO_REFERENCE_LOCALITY foreign key (locality_id)
      references Locality (locality_id)
      on delete restrict on update restrict;

alter table Locality
   add constraint FK_LOCALITY_REFERENCE_DISTRICT foreign key (district_id)
      references District (district_id)
      on delete restrict on update restrict;

alter table Locality
   add constraint FK_LOCALITY_REFERENCE_TER_TYPE foreign key (type_id)
      references Ter_type_name (type_id)
      on delete restrict on update restrict;

alter table Participants
   add constraint FK_PARTICIP_REFERENCE_CLASS_PR foreign key (profile_id)
      references Class_profiles (profile_id)
      on delete restrict on update restrict;

alter table Participants
   add constraint FK_PARTICIP_REFERENCE_PARTICIP foreign key (status_id)
      references Participant_status (status_id)
      on delete restrict on update restrict;

alter table Participants
   add constraint FK_PARTICIP_REFERENCE_LANGUAGE foreign key (lang_id)
      references Languages (lang_id)
      on delete restrict on update restrict;

alter table Participants
   add constraint FK_PARTICIP_REFERENCE_EDUCATIO foreign key (institution_id)
      references Educational_institution (institution_id)
      on delete restrict on update restrict;

alter table Participants
   add constraint FK_PARTICIP_REFERENCE_LOCALITY foreign key (locality_id)
      references Locality (locality_id)
      on delete restrict on update restrict;

alter table Passing_exam
   add constraint FK_PASSING__REFERENCE_PARTICIP foreign key (out_id)
      references Participants (out_id)
      on delete restrict on update restrict;

alter table Passing_exam
   add constraint FK_PASSING__REFERENCE_SUBJECTS foreign key (subject_id)
      references Subjects (subject_id)
      on delete restrict on update restrict;

alter table Passing_exam
   add constraint FK_PASSING__REFERENCE_EDUCATIO foreign key (institution_id)
      references Educational_institution (institution_id)
      on delete restrict on update restrict;

alter table Passing_exam
   add constraint FK_PASSING__REFERENCE_LANGUAGE foreign key (lang_id)
      references Languages (lang_id)
      on delete restrict on update restrict;

