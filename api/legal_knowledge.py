"""
Indian Legal Knowledge Base
Comprehensive database of Indian laws, constitution articles, and legal procedures.
Used by the NLP pipeline for retrieval-augmented generation.
"""

LEGAL_KNOWLEDGE_BASE = {
    "constitution": [
        {
            "id": "article-14",
            "title": "Article 14 — Right to Equality",
            "category": "constitution",
            "subcategory": "fundamental_rights",
            "content": "The State shall not deny to any person equality before the law or the equal protection of the laws within the territory of India.",
            "explanation": "Article 14 is the foundation of India's commitment to equality. It guarantees two things: (1) Equality before the law — no one is above the law, and (2) Equal protection of laws — similar treatment in similar circumstances. This right applies to all persons in India, not just citizens. However, reasonable classification is allowed if it is based on intelligible differentia and has a rational nexus with the object of the legislation.",
            "guidance": [
                "This right applies to all persons in India, not just citizens",
                "The State cannot make unreasonable distinctions between people",
                "Reasonable classification based on intelligible differentia is allowed",
                "Any discrimination can be challenged in courts through writ petitions under Article 32 or Article 226"
            ],
            "keywords": ["equality", "discrimination", "equal protection", "fundamental rights", "article 14", "constitution", "writ petition", "reasonable classification"],
            "related": ["article-15", "article-16", "article-32"]
        },
        {
            "id": "article-15",
            "title": "Article 15 — Prohibition of Discrimination",
            "category": "constitution",
            "subcategory": "fundamental_rights",
            "content": "The State shall not discriminate against any citizen on grounds only of religion, race, caste, sex, place of birth or any of them.",
            "explanation": "Article 15 prohibits discrimination by the State on grounds of religion, race, caste, sex, or place of birth. It also forbids any restriction on access to public places like shops, restaurants, wells, tanks, roads, and places of public resort. Importantly, the State can make special provisions for women, children, and socially/educationally backward classes (through reservations).",
            "guidance": [
                "Discrimination on grounds of religion, race, caste, sex, or place of birth is prohibited",
                "Special provisions for women and children are permitted",
                "Reservation for backward classes is constitutionally valid under Articles 15(4) and 15(5)",
                "Applies to State action and access to public places"
            ],
            "keywords": ["discrimination", "caste", "religion", "sex", "reservation", "backward classes", "article 15", "fundamental rights"],
            "related": ["article-14", "article-16", "article-17"]
        },
        {
            "id": "article-19",
            "title": "Article 19 — Protection of Six Freedoms",
            "category": "constitution",
            "subcategory": "fundamental_rights",
            "content": "All citizens shall have the right to: (a) freedom of speech and expression, (b) assemble peaceably and without arms, (c) form associations or unions, (d) move freely throughout the territory of India, (e) reside and settle in any part of the territory of India, (f) practise any profession, or to carry on any occupation, trade or business.",
            "explanation": "Article 19 is one of the most important fundamental rights, protecting six freedoms essential for a democratic society. These rights are available only to Indian citizens (not foreigners). However, the State can impose reasonable restrictions on these freedoms in the interest of sovereignty, integrity of India, security of the State, public order, decency, morality, or other grounds specified in Article 19(2) to 19(6).",
            "guidance": [
                "These rights are available only to citizens, not to foreigners",
                "Reasonable restrictions can be imposed by the State",
                "Freedom of speech includes right to information and freedom of press",
                "Right to practise any profession is subject to professional and technical qualifications",
                "Right to form associations includes trade unions and political parties"
            ],
            "keywords": ["freedom", "speech", "expression", "assembly", "movement", "profession", "article 19", "fundamental rights", "press freedom", "trade union"],
            "related": ["article-19a", "article-21", "article-25"]
        },
        {
            "id": "article-21",
            "title": "Article 21 — Right to Life and Personal Liberty",
            "category": "constitution",
            "subcategory": "fundamental_rights",
            "content": "No person shall be deprived of his life or personal liberty except according to procedure established by law.",
            "explanation": "Article 21 is the most expansive fundamental right in the Indian Constitution. Through judicial interpretation, the Supreme Court has read into it the right to live with human dignity, right to livelihood, right to privacy (Puttaswamy case, 2017), right to clean environment, right to health, right to education, right to shelter, right to legal aid, and right against solitary confinement. This right cannot be suspended even during a national emergency.",
            "guidance": [
                "This right cannot be suspended even during emergency",
                "Includes right to live with dignity, not mere animal existence",
                "Right to privacy is recognized as part of Article 21 (Puttaswamy, 2017)",
                "Free legal aid must be provided under Article 21 read with Article 39A",
                "Right to speedy trial is part of Article 21",
                "Procedure must be just, fair, and reasonable (Maneka Gandhi case)"
            ],
            "keywords": ["life", "liberty", "due process", "dignity", "privacy", "article 21", "fundamental rights", "puttaswamy", "maneka gandhi", "right to health", "right to education"],
            "related": ["article-21a", "article-22", "article-32"]
        },
        {
            "id": "article-21a",
            "title": "Article 21A — Right to Education",
            "category": "constitution",
            "subcategory": "fundamental_rights",
            "content": "The State shall provide free and compulsory education to all children of the age of six to fourteen years in such manner as the State may, by law, determine.",
            "explanation": "Added by the 86th Constitutional Amendment Act, 2002, Article 21A makes free and compulsory education a fundamental right for children aged 6-14 years. The Right of Children to Free and Compulsory Education Act, 2009 (RTE Act) provides the legislative framework. Schools must reserve 25% seats for economically weaker sections.",
            "guidance": [
                "Free and compulsory education for children aged 6-14 years",
                "RTE Act 2009 provides detailed implementation framework",
                "25% reservation in private schools for economically weaker sections",
                "No child can be denied admission or failed until Class 8",
                "Schools must maintain prescribed pupil-teacher ratio"
            ],
            "keywords": ["education", "RTE", "right to education", "children", "free education", "compulsory education", "article 21a", "amendment"],
            "related": ["article-21", "article-45", "article-51a"]
        },
        {
            "id": "article-22",
            "title": "Article 22 — Protection Against Arrest and Detention",
            "category": "constitution",
            "subcategory": "fundamental_rights",
            "content": "No person who is arrested shall be detained in custody without being informed of the grounds for such arrest. Every person arrested shall have the right to consult and be defended by a legal practitioner of his choice.",
            "explanation": "Article 22 provides important safeguards against arbitrary arrest and detention. It mandates that arrested persons must be informed of the grounds of arrest, allowed to consult a lawyer, and produced before a magistrate within 24 hours. It also regulates preventive detention, requiring that detention beyond 3 months must be reviewed by an Advisory Board.",
            "guidance": [
                "Arrested person must be informed of grounds of arrest immediately",
                "Right to consult and be defended by a lawyer of choice",
                "Must be produced before nearest magistrate within 24 hours",
                "Preventive detention cannot exceed 3 months without Advisory Board review",
                "These rights do not apply to enemy aliens or persons under preventive detention laws"
            ],
            "keywords": ["arrest", "detention", "lawyer", "magistrate", "24 hours", "preventive detention", "article 22", "fundamental rights", "bail"],
            "related": ["article-21", "article-32", "section-436"]
        },
        {
            "id": "article-25",
            "title": "Article 25 — Freedom of Religion",
            "category": "constitution",
            "subcategory": "fundamental_rights",
            "content": "Subject to public order, morality and health, all persons are equally entitled to freedom of conscience and the right freely to profess, practise and propagate religion.",
            "explanation": "Article 25 guarantees freedom of conscience and the right to freely profess, practise, and propagate religion to all persons in India. This right is subject to public order, morality, health, and other fundamental rights. The State can regulate or restrict any economic, financial, political, or other secular activity associated with religious practice.",
            "guidance": [
                "Right to profess, practise and propagate religion",
                "Subject to public order, morality and health",
                "State can regulate secular aspects of religious activity",
                "Hindu temples can be thrown open to all classes by law",
                "Wearing of kirpans is included in profession of Sikh religion"
            ],
            "keywords": ["religion", "freedom of religion", "conscience", "propagate", "article 25", "fundamental rights", "secularism"],
            "related": ["article-26", "article-27", "article-28"]
        },
        {
            "id": "article-32",
            "title": "Article 32 — Right to Constitutional Remedies",
            "category": "constitution",
            "subcategory": "fundamental_rights",
            "content": "The right to move the Supreme Court by appropriate proceedings for the enforcement of fundamental rights is guaranteed. The Supreme Court shall have power to issue directions, orders or writs for enforcement of any fundamental rights.",
            "explanation": "Article 32 is called the 'heart and soul' of the Constitution by Dr. B.R. Ambedkar. It provides a guaranteed remedy for enforcement of fundamental rights through the Supreme Court. The Court can issue five types of writs: Habeas Corpus (release from illegal detention), Mandamus (command to perform duty), Prohibition (prevent lower court from exceeding jurisdiction), Certiorari (quash order of lower court), and Quo Warranto (challenge unauthorized holding of office).",
            "guidance": [
                "Direct access to Supreme Court for fundamental rights violations",
                "Five writs: Habeas Corpus, Mandamus, Prohibition, Certiorari, Quo Warranto",
                "This right itself is a fundamental right that cannot be suspended",
                "Article 226 gives similar powers to High Courts",
                "PIL (Public Interest Litigation) is an extension of Article 32"
            ],
            "keywords": ["constitutional remedies", "writs", "supreme court", "enforcement", "article 32", "habeas corpus", "mandamus", "PIL", "public interest litigation", "ambedkar"],
            "related": ["article-226", "article-21", "article-14"]
        },
        {
            "id": "article-44",
            "title": "Article 44 — Uniform Civil Code",
            "category": "constitution",
            "subcategory": "dpsp",
            "content": "The State shall endeavour to secure for the citizens a uniform civil code throughout the territory of India.",
            "explanation": "Article 44 is a Directive Principle of State Policy that directs the State to work towards a Uniform Civil Code (UCC) for all citizens. Currently, different religious communities in India are governed by their own personal laws in matters of marriage, divorce, inheritance, and succession. The UCC aims to replace these diverse personal laws with a common set of laws applicable to all citizens. Goa is the only Indian state with a UCC.",
            "guidance": [
                "Directive Principle — not enforceable in court but fundamental in governance",
                "Aims to replace diverse personal laws with a common code",
                "Currently debated extensively in Indian political and social discourse",
                "Goa already has a Uniform Civil Code",
                "Supreme Court has recommended implementation in several cases"
            ],
            "keywords": ["uniform civil code", "UCC", "personal law", "directive principle", "article 44", "DPSP"],
            "related": ["article-25", "article-37"]
        },
        {
            "id": "article-370",
            "title": "Article 370 — Special Status of Jammu & Kashmir (Abrogated)",
            "category": "constitution",
            "subcategory": "special_provisions",
            "content": "Article 370 granted special autonomous status to the state of Jammu and Kashmir. It was abrogated on 5 August 2019 through a Presidential Order.",
            "explanation": "Article 370 provided special status to J&K, giving the state its own constitution, a separate flag, and autonomy over all matters except defence, foreign affairs, and communications. On 5 August 2019, the Government of India revoked Article 370 through Constitutional Order 272, effectively integrating J&K fully with the Indian Union. The state was also reorganised into two Union Territories: Jammu & Kashmir (with legislature) and Ladakh (without legislature). The Supreme Court upheld this decision in December 2023.",
            "guidance": [
                "Article 370 was abrogated on 5 August 2019",
                "J&K reorganised into two Union Territories",
                "Supreme Court upheld the abrogation in December 2023",
                "All provisions of the Indian Constitution now apply to J&K",
                "Article 35A (differential treatment for permanent residents) also abrogated"
            ],
            "keywords": ["article 370", "jammu kashmir", "special status", "abrogation", "union territory", "article 35a"],
            "related": ["article-1", "article-3"]
        }
    ],

    "criminal": {
        "ipc": [
            {
                "id": "section-302",
                "title": "Section 302 IPC — Murder",
                "category": "criminal",
                "subcategory": "ipc",
                "content": "Whoever commits murder shall be punished with death, or imprisonment for life, and shall also be liable to fine.",
                "explanation": "Section 302 prescribes punishment for murder, which is the most serious offence under the IPC. Murder is defined in Section 300 as culpable homicide amounting to murder when done with intention to cause death, or with intention to cause bodily injury known to be likely to cause death, or with knowledge that the act is so imminently dangerous that it must in all probability cause death. The difference between murder (Section 302) and culpable homicide not amounting to murder (Section 304) lies in the degree of intention and knowledge.",
                "guidance": [
                    "Murder requires intention to cause death or knowledge of likely death",
                    "Distinguished from culpable homicide (Section 304) by degree of intention",
                    "Punishment: death penalty or life imprisonment plus fine",
                    "Life imprisonment means imprisonment for the remainder of natural life",
                    "Investigation conducted by police, trial in Sessions Court"
                ],
                "keywords": ["murder", "homicide", "death penalty", "life imprisonment", "section 302", "ipc", "killing", "intention"],
                "related": ["section-300", "section-304", "section-307"]
            },
            {
                "id": "section-304a",
                "title": "Section 304A IPC — Death by Negligence",
                "category": "criminal",
                "subcategory": "ipc",
                "content": "Whoever causes the death of any person by doing any rash or negligent act not amounting to culpable homicide, shall be punished with imprisonment up to two years, or with fine, or with both.",
                "explanation": "Section 304A covers cases where death is caused by negligence or rashness, but without any intention to cause death. Common examples include road accidents due to reckless driving, medical negligence leading to death, and industrial accidents due to safety violations. The key distinction from murder/culpable homicide is the complete absence of intention or knowledge that the act might cause death.",
                "guidance": [
                    "Covers death caused by negligence without intention",
                    "Common in road accidents and medical negligence cases",
                    "Punishment: up to 2 years imprisonment and/or fine",
                    "Bailable and compoundable offence in many cases",
                    "Motor Vehicles Act provisions may also apply in road accidents"
                ],
                "keywords": ["negligence", "death by negligence", "rash driving", "medical negligence", "accident", "section 304a", "ipc"],
                "related": ["section-302", "section-304", "section-279"]
            },
            {
                "id": "section-376",
                "title": "Section 376 IPC — Rape",
                "category": "criminal",
                "subcategory": "ipc",
                "content": "Whoever commits rape shall be punished with rigorous imprisonment for a term not less than ten years but which may extend to imprisonment for life, and shall also be liable to fine.",
                "explanation": "After the Criminal Law (Amendment) Act, 2013 (following the Nirbhaya case), Section 376 was significantly strengthened. The minimum punishment was increased to 10 years. Gang rape carries minimum 20 years. Rape of a minor under 12 years can attract death penalty (added in 2018). The definition of rape was expanded. Marital rape of a wife above 15 years (now 18) was not initially covered but remains debated.",
                "guidance": [
                    "Minimum punishment: 10 years rigorous imprisonment",
                    "Gang rape (Section 376D): minimum 20 years",
                    "Rape of minor under 12: can attract death penalty",
                    "Immediate medical examination and FIR filing is crucial",
                    "Victim's identity is protected by law",
                    "Special fast-track courts handle rape cases"
                ],
                "keywords": ["rape", "sexual assault", "section 376", "ipc", "nirbhaya", "victim protection", "fast track court", "POCSO"],
                "related": ["section-354", "section-376d", "pocso-act"]
            },
            {
                "id": "section-420",
                "title": "Section 420 IPC — Cheating and Dishonestly Inducing Delivery of Property",
                "category": "criminal",
                "subcategory": "ipc",
                "content": "Whoever cheats and thereby dishonestly induces the person deceived to deliver any property to any person, or to make, alter or destroy any valuable security, shall be punished with imprisonment up to seven years and shall also be liable to fine.",
                "explanation": "Section 420 is one of the most frequently invoked sections in India for fraud cases. It combines cheating (defined in Section 415) with dishonest inducement to deliver property. This section covers financial frauds, property scams, fake documentation, online frauds, insurance frauds, and investment scams. The prosecution must prove both the act of deception and the resulting delivery/destruction of property or valuable security.",
                "guidance": [
                    "File FIR immediately with all evidence and documentation",
                    "Preserve all communications, receipts, and transaction records",
                    "Can be filed online in many states through citizen portals",
                    "Punishment: up to 7 years imprisonment plus fine",
                    "Non-bailable offence — bail is at court's discretion",
                    "Consider filing complaint in Economic Offences Court for large financial frauds"
                ],
                "keywords": ["cheating", "fraud", "dishonesty", "property", "deception", "financial crime", "section 420", "ipc", "scam", "online fraud"],
                "related": ["section-415", "section-406", "section-468"]
            },
            {
                "id": "section-498a",
                "title": "Section 498A IPC — Cruelty by Husband or Relatives",
                "category": "criminal",
                "subcategory": "ipc",
                "content": "Whoever, being the husband or the relative of the husband of a woman, subjects such woman to cruelty shall be punished with imprisonment for a term which may extend to three years and shall also be liable to fine.",
                "explanation": "Section 498A addresses domestic violence and cruelty against married women. Cruelty includes both physical violence and mental harassment, especially in connection with demands for dowry. This section is cognizable (police can arrest without warrant), non-bailable, and non-compoundable. The Supreme Court in Rajesh Sharma case (2017) introduced certain safeguards against misuse, including requiring a Family Welfare Committee review before arrest.",
                "guidance": [
                    "Covers both mental and physical cruelty against married women",
                    "Cognizable and non-bailable offence",
                    "Domestic Violence Act 2005 provides additional civil remedies",
                    "Protection officers and shelter homes available for victims",
                    "Women helpline: 181, Police: 100",
                    "Supreme Court safeguards against misuse (Rajesh Sharma case)"
                ],
                "keywords": ["domestic violence", "cruelty", "dowry", "harassment", "women protection", "section 498a", "ipc", "marriage", "husband"],
                "related": ["section-304b", "section-406", "dv-act-2005"]
            },
            {
                "id": "section-379",
                "title": "Section 379 IPC — Theft",
                "category": "criminal",
                "subcategory": "ipc",
                "content": "Whoever commits theft shall be punished with imprisonment of either description for a term which may extend to three years, or with fine, or with both.",
                "explanation": "Theft under Section 378 IPC requires: (1) dishonest intention to take property, (2) the property must be movable, (3) taken out of the possession of another person, (4) without that person's consent, and (5) some moving of the property. Section 379 prescribes the punishment. Aggravated forms include theft in a dwelling house (Section 380), theft by clerk/servant (Section 381), and theft after preparation for causing death/hurt (Section 382).",
                "guidance": [
                    "Theft requires dishonest intention and actual taking of property",
                    "Property must be movable and taken without owner's consent",
                    "Punishment: up to 3 years imprisonment and/or fine",
                    "File FIR immediately with details of stolen items",
                    "Aggravated theft carries higher penalties",
                    "Vehicle theft — also file complaint with RTO"
                ],
                "keywords": ["theft", "stealing", "movable property", "dishonest intention", "section 379", "ipc", "robbery", "burglary"],
                "related": ["section-378", "section-380", "section-392"]
            },
            {
                "id": "section-354",
                "title": "Section 354 IPC — Assault on Woman to Outrage Modesty",
                "category": "criminal",
                "subcategory": "ipc",
                "content": "Whoever assaults or uses criminal force to any woman, intending to outrage or knowing it to be likely that he will thereby outrage her modesty, shall be punished with imprisonment of not less than one year but which may extend to five years, and shall also be liable to fine.",
                "explanation": "Section 354 protects women from sexual harassment and molestation. After the 2013 Amendment, specific sub-sections were added: 354A (sexual harassment including unwelcome physical contact, demands for sexual favours), 354B (assault with intent to disrobe), 354C (voyeurism), and 354D (stalking). These amendments significantly strengthened legal protection for women.",
                "guidance": [
                    "Minimum punishment: 1 year, maximum: 5 years imprisonment",
                    "Section 354A: Sexual harassment at workplace — up to 3 years",
                    "Section 354D: Stalking — up to 3 years for first offence",
                    "File complaint immediately — cognizable offence",
                    "Workplace harassment: also file under POSH Act",
                    "Women helpline: 181"
                ],
                "keywords": ["molestation", "sexual harassment", "modesty", "stalking", "voyeurism", "section 354", "ipc", "women safety", "POSH"],
                "related": ["section-376", "section-509", "posh-act"]
            },
            {
                "id": "section-307",
                "title": "Section 307 IPC — Attempt to Murder",
                "category": "criminal",
                "subcategory": "ipc",
                "content": "Whoever does any act with such intention or knowledge, and under such circumstances that, if he by that act caused death he would be guilty of murder, shall be punished with imprisonment up to ten years and fine. If hurt is caused, the punishment may extend to imprisonment for life.",
                "explanation": "Section 307 covers attempt to murder — where the accused intended to cause death but the victim survived. The prosecution must prove that the act was done with the intention or knowledge that it was likely to cause death. If the act causes hurt to the victim, the punishment can be enhanced to life imprisonment. The section requires the act to be of such a nature that it would have resulted in murder had death occurred.",
                "guidance": [
                    "Requires intention or knowledge that act may cause death",
                    "Punishment: up to 10 years or life imprisonment if hurt caused",
                    "Non-bailable offence — tried in Sessions Court",
                    "Previous enmity and motive are important for prosecution",
                    "Medical evidence of injuries is crucial"
                ],
                "keywords": ["attempt to murder", "attempted murder", "section 307", "ipc", "intention", "knowledge", "hurt"],
                "related": ["section-302", "section-324", "section-326"]
            }
        ],

        "crpc": [
            {
                "id": "section-154",
                "title": "Section 154 CrPC — FIR (First Information Report)",
                "category": "criminal",
                "subcategory": "crpc",
                "content": "Every information relating to the commission of a cognizable offence, if given orally to an officer in charge of a police station, shall be reduced to writing by him or under his direction, and be read over to the informant.",
                "explanation": "Section 154 CrPC is the foundation of criminal investigation in India. It mandates that police MUST register an FIR when information about a cognizable offence is received. The Supreme Court in Lalita Kumari v. State of UP (2014) held that registration of FIR is mandatory under Section 154 when information discloses commission of a cognizable offence. Police cannot refuse to register an FIR. If they do, the complainant can approach the Superintendent of Police or a Judicial Magistrate under Section 156(3).",
                "guidance": [
                    "Police MUST register FIR for cognizable offences — cannot refuse",
                    "FIR must be registered at the police station where the offence occurred",
                    "Free copy of FIR must be given to the informant",
                    "If police refuse, approach SP or file complaint under Section 156(3) before Magistrate",
                    "Zero FIR: FIR can be registered at any police station regardless of jurisdiction",
                    "E-FIR facility available in many states for certain offences",
                    "Lalita Kumari case: mandatory registration is settled law"
                ],
                "keywords": ["FIR", "first information report", "cognizable offence", "police station", "complaint", "section 154", "crpc", "zero FIR", "lalita kumari"],
                "related": ["section-155", "section-156", "section-190"]
            },
            {
                "id": "section-41",
                "title": "Section 41 CrPC — When Police May Arrest Without Warrant",
                "category": "criminal",
                "subcategory": "crpc",
                "content": "Any police officer may without an order from a Magistrate and without a warrant, arrest any person in specific circumstances including cognizable offences, proclaimed offenders, or possession of stolen property.",
                "explanation": "Section 41 was significantly amended in 2009 (Arnesh Kumar guidelines) to prevent unnecessary arrests. Now, for offences punishable with imprisonment up to 7 years, police must record reasons for arrest. The Supreme Court in Arnesh Kumar v. State of Bihar (2014) further mandated that police must be satisfied that arrest is necessary to prevent further offence, evidence tampering, or witness influencing.",
                "guidance": [
                    "Police can arrest without warrant for cognizable offences",
                    "For offences with punishment up to 7 years, arrest is not automatic",
                    "Police must record reasons for believing arrest is necessary",
                    "Arnesh Kumar guidelines mandate restraint in arrests",
                    "Arrested person must be produced before magistrate within 24 hours",
                    "Notice of arrest must be sent to family/friend under Section 41B"
                ],
                "keywords": ["arrest", "warrant", "police", "cognizable offence", "arnesh kumar", "section 41", "crpc", "arrest guidelines"],
                "related": ["section-154", "section-436", "section-437"]
            },
            {
                "id": "section-436",
                "title": "Section 436 CrPC — Bail in Bailable Offences",
                "category": "criminal",
                "subcategory": "crpc",
                "content": "When any person other than a person accused of a non-bailable offence is arrested or detained without warrant by an officer in charge of a police station, or appears or is brought before a Court, and is prepared to give bail, such person shall be released on bail.",
                "explanation": "Section 436 establishes that bail in bailable offences is a matter of RIGHT, not discretion. The police officer or court MUST release the accused on bail. The only requirement is that the accused executes a bail bond with or without sureties. If the accused is indigent and cannot furnish surety, they should be released on personal bond. Refusal of bail in bailable offences is illegal.",
                "guidance": [
                    "Bail is a RIGHT in bailable offences — cannot be refused",
                    "Police officer at the station can grant bail",
                    "If accused cannot furnish surety, release on personal bond",
                    "No conditions like passport surrender for bailable offences",
                    "Magistrate must grant bail if police refuse"
                ],
                "keywords": ["bail", "bailable offence", "personal bond", "surety", "section 436", "crpc", "right to bail"],
                "related": ["section-437", "section-439", "section-167"]
            },
            {
                "id": "section-437",
                "title": "Section 437 CrPC — Bail in Non-Bailable Offences",
                "category": "criminal",
                "subcategory": "crpc",
                "content": "When any person accused of, or suspected of, the commission of any non-bailable offence is arrested or detained without warrant, he may be released on bail by the Court, but not as of right.",
                "explanation": "Unlike bailable offences, bail in non-bailable offences is at the discretion of the court. The court considers: nature and gravity of the offence, evidence strength, likelihood of the accused fleeing justice, impact on witnesses, and criminal history. Special consideration is given to women, children below 16, and sick/infirm accused. Even in non-bailable offences, bail is the rule and jail is the exception (State of Rajasthan v. Balchand, 1977).",
                "guidance": [
                    "Bail in non-bailable offences is discretionary, not a right",
                    "Court considers nature of offence, evidence, flight risk",
                    "Special consideration for women, children, sick, and elderly",
                    "Bail is the rule, jail is the exception (Supreme Court)",
                    "High Courts have wider powers under Section 439",
                    "Anticipatory bail available under Section 438"
                ],
                "keywords": ["non-bailable offence", "discretionary bail", "court discretion", "section 437", "crpc", "bail conditions"],
                "related": ["section-436", "section-438", "section-439"]
            },
            {
                "id": "section-438",
                "title": "Section 438 CrPC — Anticipatory Bail",
                "category": "criminal",
                "subcategory": "crpc",
                "content": "Where any person has reason to believe that he may be arrested on accusation of having committed a non-bailable offence, he may apply to the High Court or the Court of Session for a direction that in the event of such arrest, he shall be released on bail.",
                "explanation": "Anticipatory bail is a pre-arrest bail provision unique to Indian criminal law. It allows a person who apprehends arrest to secure bail in advance. The court may impose conditions like making oneself available for interrogation, not making inducements to witnesses, not leaving India without permission, etc. The Supreme Court in Sushila Aggarwal v. State (2020) held that anticipatory bail can be granted without time limit.",
                "guidance": [
                    "Application must be filed before arrest occurs",
                    "Available only for non-bailable offences",
                    "Can be filed in Sessions Court or High Court",
                    "Court may impose conditions like surrender of passport",
                    "Not available in some states for certain offences",
                    "No time limit — can continue until end of trial (Sushila Aggarwal case)"
                ],
                "keywords": ["anticipatory bail", "pre-arrest bail", "section 438", "crpc", "non-bailable", "apprehension of arrest"],
                "related": ["section-437", "section-439", "section-41"]
            },
            {
                "id": "section-125",
                "title": "Section 125 CrPC — Maintenance of Wives, Children, and Parents",
                "category": "criminal",
                "subcategory": "crpc",
                "content": "If any person having sufficient means neglects or refuses to maintain his wife, unable to maintain herself, or his legitimate or illegitimate minor child, or his legitimate or illegitimate child who has attained majority but is unable to maintain itself by reason of physical or mental abnormality or injury, or his father or mother, unable to maintain himself or herself, a Magistrate may order such person to make a monthly allowance.",
                "explanation": "Section 125 is a social welfare legislation that provides a quick and effective remedy for maintenance. It applies to all persons irrespective of religion. Maintenance includes food, clothing, shelter, education, and medical treatment. The maximum maintenance amount is not specified and depends on the financial capacity of the person and reasonable needs of the claimant.",
                "guidance": [
                    "Applies irrespective of religion — even Muslims can claim (Shah Bano case)",
                    "Wife, children (including illegitimate), and parents can claim",
                    "Proceedings are before the Magistrate's Court",
                    "Interim maintenance can be awarded within 60 days",
                    "Non-payment can lead to imprisonment",
                    "Wife ceases to be entitled if she remarries or lives in adultery"
                ],
                "keywords": ["maintenance", "alimony", "wife maintenance", "child support", "parent maintenance", "section 125", "crpc", "shah bano"],
                "related": ["hindu-marriage-act", "dv-act-2005"]
            }
        ],

        "procedures": [
            {
                "id": "fir-filing",
                "title": "How to File an FIR (First Information Report)",
                "category": "criminal",
                "subcategory": "procedure",
                "content": "Complete step-by-step guide to filing an FIR in India",
                "explanation": "An FIR (First Information Report) is the first step to set the criminal law machinery in motion. It is a written document prepared by police based on information received about a cognizable offence. Filing an FIR is your legal right, and police cannot refuse to register it.",
                "steps": [
                    "Visit the nearest police station in whose jurisdiction the crime occurred",
                    "Clearly state the facts: date, time, place, description of the incident",
                    "Identify the accused if known, or provide description",
                    "The SHO/officer must write down your complaint and read it back to you",
                    "Verify the details and sign the FIR or provide thumb impression",
                    "Collect a FREE copy of the FIR — this is your right",
                    "Note down the FIR number, date, and name of the investigating officer",
                    "If police refuse, file a written complaint to the SP/DCP or approach Magistrate under Section 156(3)",
                    "Zero FIR: You can file at ANY police station — they must accept and transfer",
                    "E-FIR available in many states for property crimes and vehicle theft"
                ],
                "keywords": ["FIR", "police complaint", "how to file FIR", "first information report", "police station", "cognizable offence", "zero FIR", "e-FIR"],
                "related": ["section-154", "section-155", "section-156"]
            },
            {
                "id": "bail-process",
                "title": "Bail Application Process",
                "category": "criminal",
                "subcategory": "procedure",
                "content": "Complete guide to applying for bail in criminal cases in India",
                "explanation": "Bail is the release of an accused person from custody, subject to certain conditions ensuring their appearance at trial. The Indian legal system follows the principle 'bail is the rule, jail is the exception.'",
                "steps": [
                    "Engage a qualified criminal lawyer immediately after arrest",
                    "Determine the type of offence: bailable or non-bailable",
                    "For bailable offences: Apply at the police station itself — bail is a RIGHT",
                    "For non-bailable offences: File bail application in appropriate court",
                    "Prepare bail application with: case details, grounds for bail, personal details, sureties",
                    "Court hearing: lawyer argues for bail based on merits and legal precedents",
                    "If bail granted: execute bail bond and furnish sureties as directed",
                    "Collect bail order and present at jail for release",
                    "Comply with ALL bail conditions (court appearances, no tampering with evidence)",
                    "If denied by lower court: appeal to High Court under Section 439"
                ],
                "keywords": ["bail", "bail application", "how to get bail", "criminal lawyer", "surety", "bail bond", "bail conditions", "anticipatory bail"],
                "related": ["section-436", "section-437", "section-438", "section-439"]
            },
            {
                "id": "complaint-magistrate",
                "title": "Filing a Private Complaint Before Magistrate",
                "category": "criminal",
                "subcategory": "procedure",
                "content": "How to file a criminal complaint directly before a Magistrate when police refuse to act",
                "explanation": "When police refuse to register an FIR or investigate properly, citizens can approach a Judicial Magistrate directly under Section 190 and Section 200 CrPC. This is a powerful remedy that bypasses police inaction.",
                "steps": [
                    "Prepare a written complaint detailing the offence with all facts",
                    "Attach supporting evidence: documents, photos, witness details",
                    "File the complaint before the Judicial Magistrate of appropriate jurisdiction",
                    "Magistrate examines the complainant and witnesses under Section 200",
                    "If satisfied, Magistrate may order investigation under Section 156(3)",
                    "Alternatively, Magistrate can take cognizance and issue process directly",
                    "Accused is summoned and trial proceeds in Magistrate's Court",
                    "This remedy is effective when police refuse to act or are biased"
                ],
                "keywords": ["private complaint", "magistrate complaint", "section 200", "section 156(3)", "police inaction", "judicial magistrate"],
                "related": ["section-154", "section-190", "section-200"]
            }
        ]
    },

    "civil": [
        {
            "id": "contract-law",
            "title": "Indian Contract Act, 1872 — Contract Basics",
            "category": "civil",
            "subcategory": "contracts",
            "content": "A contract is an agreement enforceable by law. Every agreement which is made by the free consent of parties competent to contract, for a lawful consideration and with a lawful object, and which is not expressly declared to be void, is a contract.",
            "explanation": "The Indian Contract Act, 1872 governs all contracts in India. A valid contract requires: (1) offer and acceptance, (2) free consent (without coercion, undue influence, fraud, misrepresentation, or mistake), (3) parties competent to contract (age of majority, sound mind), (4) lawful consideration, (5) lawful object, and (6) not expressly declared void. Breach of contract gives the aggrieved party right to damages, specific performance, or rescission.",
            "guidance": [
                "Valid contract requires: offer, acceptance, consideration, competent parties",
                "Minors (below 18) cannot enter into contracts",
                "Contracts obtained by coercion, fraud, or undue influence are voidable",
                "Breach of contract remedies: damages, specific performance, injunction",
                "Written contracts are easier to enforce but oral contracts are also valid",
                "Limitation period for breach of contract is 3 years"
            ],
            "keywords": ["contract", "agreement", "consideration", "breach", "damages", "contract act", "civil law", "offer", "acceptance", "void", "voidable"],
            "related": ["specific-relief-act", "limitation-act"]
        },
        {
            "id": "property-rights",
            "title": "Property Rights and Transfer of Property",
            "category": "civil",
            "subcategory": "property",
            "content": "Property rights in India are governed by the Transfer of Property Act 1882, Registration Act 1908, and various state-specific land laws.",
            "explanation": "The Transfer of Property Act, 1882 governs transfer of property by act of parties (as opposed to transfer by operation of law). It covers sale, mortgage, lease, exchange, and gifts of immovable property. All transfers of immovable property valued above Rs. 100 must be registered under the Registration Act, 1908. Due diligence before property purchase includes: title search, encumbrance certificate, approved layout, tax receipts, and mutation entries.",
            "guidance": [
                "Property registration is mandatory for immovable property",
                "Stamp duty varies by state — typically 5-7% of property value",
                "Always verify clear title through title search at Sub-Registrar's office",
                "Obtain encumbrance certificate for at least 30 years",
                "Verify approved layout and building permissions from local authority",
                "Property disputes can be resolved through civil courts",
                "Limitation period for property suits is typically 12 years"
            ],
            "keywords": ["property", "title", "registration", "ownership", "transfer", "stamp duty", "encumbrance", "civil law", "sale deed", "land"],
            "related": ["registration-act", "limitation-act", "rent-control"]
        },
        {
            "id": "civil-suit",
            "title": "How to File a Civil Suit",
            "category": "civil",
            "subcategory": "procedure",
            "content": "Procedure for filing a civil suit in Indian courts under the Code of Civil Procedure (CPC), 1908.",
            "explanation": "Civil suits are governed by the Code of Civil Procedure, 1908. A civil suit is filed when there is a dispute regarding civil rights like property, contracts, recovery of money, specific performance, injunction, or declaration. The suit must be filed in the court of appropriate jurisdiction (territorial and pecuniary).",
            "steps": [
                "Consult a civil lawyer and assess merits of the case",
                "Determine appropriate court jurisdiction (territorial and pecuniary)",
                "Draft the plaint (suit) with all relevant facts, cause of action, and relief sought",
                "Pay court fees based on the value of the suit",
                "File the plaint in the court registry",
                "Court issues summons to the defendant",
                "Defendant files written statement within 30 days",
                "Framing of issues by the court",
                "Evidence stage: examination and cross-examination of witnesses",
                "Final arguments and judgment"
            ],
            "keywords": ["civil suit", "plaint", "court fees", "jurisdiction", "CPC", "defendant", "summons", "judgment", "civil court"],
            "related": ["contract-law", "property-rights"]
        }
    ],

    "family": [
        {
            "id": "hindu-marriage",
            "title": "Hindu Marriage Act, 1955",
            "category": "family",
            "subcategory": "marriage",
            "content": "The Hindu Marriage Act governs marriage, divorce, maintenance, and guardianship for Hindus, Buddhists, Jains, and Sikhs.",
            "explanation": "The Hindu Marriage Act, 1955 provides for: conditions of a valid Hindu marriage, registration of marriage, restitution of conjugal rights, judicial separation, void and voidable marriages, divorce (both mutual consent and contested), maintenance pendente lite, permanent alimony, and custody of children. The Act applies to Hindus, Buddhists, Jains, and Sikhs.",
            "guidance": [
                "Minimum marriage age: 21 for groom, 18 for bride",
                "Sapinda relationship and prohibited degree marriages are void",
                "Bigamy is punishable under Section 494/495 IPC",
                "Marriage registration recommended (mandatory in many states)",
                "Divorce available on grounds: cruelty, desertion, conversion, mental disorder, etc.",
                "Mutual consent divorce requires 6-month cooling period",
                "Court considers welfare of child for custody decisions"
            ],
            "keywords": ["hindu marriage", "marriage act", "divorce", "custody", "maintenance", "bigamy", "sapinda", "family law"],
            "related": ["special-marriage-act", "divorce-procedure", "section-125"]
        },
        {
            "id": "divorce-procedure",
            "title": "Divorce Procedures in India",
            "category": "family",
            "subcategory": "divorce",
            "content": "Legal procedures for obtaining divorce in India under various personal laws and the Special Marriage Act.",
            "explanation": "Divorce in India can be obtained through: (1) Mutual Consent — both parties agree (Section 13B HMA), requiring 6-18 months, or (2) Contested Divorce — one party files on specific grounds. Grounds vary by personal law but commonly include cruelty, desertion (2+ years), adultery, conversion, mental disorder (unsound mind), communicable disease, and renunciation of the world. The Supreme Court has allowed dissolution by mutual consent even during appeal (Amardeep Singh case, 2017).",
            "guidance": [
                "Mutual consent divorce: both parties agree, 6-month cooling period (can be waived)",
                "Contested divorce: must prove specific grounds like cruelty, desertion, adultery",
                "Family courts have jurisdiction over all matrimonial disputes",
                "Mediation is mandatory before contested divorce proceedings",
                "Wife entitled to maintenance during and after proceedings",
                "Custody of children decided on 'welfare of the child' principle",
                "Supreme Court can waive 6-month cooling period in mutual consent divorce"
            ],
            "keywords": ["divorce", "mutual consent", "contested divorce", "family court", "grounds for divorce", "cruelty", "desertion", "custody", "maintenance"],
            "related": ["hindu-marriage", "section-125", "dv-act-2005"]
        },
        {
            "id": "domestic-violence",
            "title": "Protection of Women from Domestic Violence Act, 2005",
            "category": "family",
            "subcategory": "women_protection",
            "content": "The DV Act provides civil remedies to women facing domestic violence including protection orders, residence orders, monetary relief, and custody orders.",
            "explanation": "The Domestic Violence Act, 2005 is a civil law that provides immediate relief to women facing domestic violence. It covers physical, sexual, verbal/emotional, and economic abuse. The Act provides several remedies: protection orders (restraining abuser), residence orders (right to live in shared household), monetary relief (maintenance, medical expenses, damages), custody orders, and compensation orders. Any woman in a domestic relationship can file a complaint, including live-in partners.",
            "guidance": [
                "Covers physical, sexual, verbal, emotional, and economic abuse",
                "Applies to wives, live-in partners, and women in domestic relationships",
                "Protection officer assists in filing complaint and obtaining orders",
                "Court must dispose of application within 60 days",
                "Interim orders can be passed ex-parte in urgent cases",
                "Breach of protection order is a criminal offence",
                "File complaint at nearest Protection Officer or Service Provider",
                "Women helpline: 181"
            ],
            "keywords": ["domestic violence", "DV act", "protection order", "residence order", "maintenance", "women protection", "abuse", "family law"],
            "related": ["section-498a", "section-125", "divorce-procedure"]
        }
    ],

    "labor": [
        {
            "id": "minimum-wages",
            "title": "Minimum Wages Act, 1948",
            "category": "labor",
            "subcategory": "wages",
            "content": "The Minimum Wages Act ensures minimum wages for workers in scheduled employments and prevents exploitation of labor.",
            "explanation": "The Minimum Wages Act, 1948 empowers both Central and State governments to fix minimum wages for workers in scheduled employments. Minimum wages vary by state, industry, and skill level. Employers who pay less than minimum wages can be prosecuted. The Act is being subsumed under the Code on Wages, 2019 which consolidates four labor laws.",
            "guidance": [
                "Minimum wages vary by state, industry, and skill level",
                "Wages must be paid in cash/cheque within prescribed time",
                "Overtime rate is typically double (2x) the normal wage",
                "Complaint for non-payment: file before Labor Commissioner",
                "Code on Wages, 2019 is replacing older wage laws",
                "Bonded labor is prohibited under the Constitution"
            ],
            "keywords": ["minimum wages", "scheduled employment", "labor inspector", "overtime", "labor law", "wages", "code on wages"],
            "related": ["epf-esi", "industrial-disputes"]
        },
        {
            "id": "epf-esi",
            "title": "EPF and ESI Benefits",
            "category": "labor",
            "subcategory": "social_security",
            "content": "Employee Provident Fund (EPF) and Employee State Insurance (ESI) provide retirement and health benefits to employees.",
            "explanation": "EPF (Employee Provident Fund) under the EPF Act, 1952, provides retirement savings where both employee and employer contribute 12% of basic salary. ESI (Employee State Insurance) under the ESI Act, 1948, provides medical benefits, sick pay, maternity benefits, and disability compensation. EPF is mandatory for establishments with 20+ employees, and ESI for establishments with 10+ employees (with wage ceiling of Rs. 21,000/month).",
            "guidance": [
                "EPF: Both employee and employer contribute 12% of basic salary",
                "ESI: Employee contributes 0.75%, employer contributes 3.25%",
                "EPF withdrawal allowed for home purchase, medical emergency, education",
                "ESI covers medical treatment, sick leave, maternity benefits",
                "Register at EPFO (epfindia.gov.in) and ESIC (esic.gov.in)",
                "Nomination must be filed for both EPF and ESI",
                "EPF can be transferred when changing jobs via UAN (Universal Account Number)"
            ],
            "keywords": ["EPF", "ESI", "provident fund", "medical benefits", "retirement", "labor law", "UAN", "EPFO", "ESIC", "social security"],
            "related": ["minimum-wages", "gratuity"]
        },
        {
            "id": "workplace-harassment",
            "title": "POSH Act — Prevention of Sexual Harassment at Workplace",
            "category": "labor",
            "subcategory": "workplace_safety",
            "content": "The Sexual Harassment of Women at Workplace (Prevention, Prohibition and Redressal) Act, 2013 mandates internal complaints committees and protects women employees.",
            "explanation": "The POSH Act, 2013 was enacted following the Supreme Court's Vishaka guidelines (1997). Every workplace with 10+ employees must have an Internal Complaints Committee (ICC). The Act covers all women employees including temporary, contractual, and interns. Sexual harassment includes unwanted physical contact, demands for sexual favours, sexually coloured remarks, showing pornography, and any unwelcome sexual behaviour.",
            "guidance": [
                "Every workplace with 10+ employees must have an Internal Complaints Committee",
                "Complaint must be filed within 3 months of the incident",
                "ICC must complete inquiry within 90 days",
                "Complainant can seek transfer or leave during inquiry",
                "False and malicious complaints are also punishable",
                "Employer can be penalized for non-compliance (up to Rs. 50,000)",
                "District Officer handles complaints for the unorganized sector"
            ],
            "keywords": ["POSH", "sexual harassment", "workplace", "ICC", "internal complaints committee", "vishaka", "women safety", "labor law"],
            "related": ["section-354", "section-509"]
        }
    ],

    "consumer": [
        {
            "id": "consumer-rights",
            "title": "Consumer Protection Act, 2019",
            "category": "consumer",
            "subcategory": "rights",
            "content": "The Consumer Protection Act, 2019 provides comprehensive protection to consumers and establishes three-tier consumer commissions for dispute resolution.",
            "explanation": "The Consumer Protection Act, 2019 replaced the 1986 Act with enhanced protections. It establishes six consumer rights: Right to Safety, Right to be Informed, Right to Choose, Right to be Heard, Right to Seek Redressal, and Right to Consumer Education. Key features include: product liability provisions, Central Consumer Protection Authority (CCPA) for class actions, e-commerce regulation, celebrity endorsement liability, and mediation as alternative dispute resolution.",
            "guidance": [
                "Six consumer rights: Safety, Information, Choice, Hearing, Redressal, Education",
                "Product liability: manufacturers, sellers, and service providers can be held liable",
                "E-commerce platforms are regulated under the Act",
                "Misleading advertisements: CCPA can impose penalty up to Rs. 50 lakh",
                "Celebrity endorsers can be held liable for misleading ads",
                "Mediation is available as alternative dispute resolution",
                "Complaints can be filed online through e-daakhil portal"
            ],
            "keywords": ["consumer rights", "consumer protection", "product liability", "e-commerce", "misleading advertisement", "CCPA", "consumer law"],
            "related": ["consumer-complaint", "food-safety"]
        },
        {
            "id": "consumer-complaint",
            "title": "Filing Consumer Complaints",
            "category": "consumer",
            "subcategory": "procedure",
            "content": "How to file consumer complaints in consumer commissions (District, State, National) for deficiency in service or defective goods.",
            "explanation": "Consumer complaints can be filed for deficiency in service, defective goods, unfair trade practices, and restrictive trade practices. The three-tier structure: District Commission (up to Rs. 1 crore), State Commission (Rs. 1-10 crores), National Commission (above Rs. 10 crores). No court fee is required for complaints up to Rs. 5 lakh. Complaints must be filed within 2 years of the cause of action.",
            "guidance": [
                "District Commission: claims up to Rs. 1 crore",
                "State Commission: claims Rs. 1 crore to Rs. 10 crores",
                "National Commission: claims above Rs. 10 crores",
                "No court fee for claims up to Rs. 5 lakh",
                "Limitation period: 2 years from cause of action",
                "File online at e-daakhil.nic.in",
                "Attach all bills, receipts, correspondence, and warranty cards",
                "Appeals: District to State (30 days), State to National (30 days)"
            ],
            "keywords": ["consumer complaint", "district commission", "state commission", "national commission", "e-daakhil", "deficiency", "defective goods", "consumer forum"],
            "related": ["consumer-rights"]
        }
    ],

    "cyber": [
        {
            "id": "it-act",
            "title": "Information Technology Act, 2000 — Cyber Crime Laws",
            "category": "cyber",
            "subcategory": "cyber_crime",
            "content": "The Information Technology Act, 2000 provides legal framework for electronic governance, digital signatures, cyber crimes, and data protection in India.",
            "explanation": "The IT Act, 2000 (amended in 2008) is India's primary law governing cyber crimes and electronic commerce. Key provisions include: Section 43 (unauthorized access and damage to computer systems — compensation up to Rs. 1 crore), Section 66 (computer related offences — up to 3 years imprisonment), Section 66A (struck down by Supreme Court in Shreya Singhal case), Section 66C (identity theft), Section 66D (cheating by personation using computer), Section 67 (publishing obscene material), and Section 72 (breach of confidentiality and privacy).",
            "guidance": [
                "Report cyber crimes at cybercrime.gov.in or call 1930",
                "Section 66C: Identity theft — up to 3 years imprisonment",
                "Section 66D: Online cheating/phishing — up to 3 years imprisonment",
                "Section 67: Publishing obscene content — up to 5 years imprisonment",
                "Section 43: Unauthorized access — compensation up to Rs. 1 crore",
                "Preserve all evidence: screenshots, URLs, transaction details",
                "File FIR at nearest Cyber Crime Police Station"
            ],
            "keywords": ["cyber crime", "IT act", "hacking", "identity theft", "phishing", "online fraud", "data protection", "section 66", "computer crime"],
            "related": ["section-420", "section-468"]
        }
    ],

    "rights": [
        {
            "id": "rti-act",
            "title": "Right to Information Act, 2005",
            "category": "rights",
            "subcategory": "transparency",
            "content": "The RTI Act empowers citizens to seek information from public authorities, promoting transparency and accountability in government.",
            "explanation": "The RTI Act, 2005 is one of India's most powerful tools for citizen empowerment and government transparency. Any citizen can request information from a 'public authority' which must respond within 30 days. The fee is just Rs. 10 for an application. Information includes records, documents, memos, emails, opinions, press releases, circulars, reports, and data in any form. Only certain categories like national security, personal privacy, and trade secrets are exempt.",
            "guidance": [
                "Application fee: Rs. 10 (BPL applicants are exempt)",
                "Response must be provided within 30 days",
                "First appeal: within 30 days to First Appellate Authority",
                "Second appeal: within 90 days to Central/State Information Commission",
                "Penalty on PIO for delay: Rs. 250 per day, maximum Rs. 25,000",
                "Online RTI filing available at rtionline.gov.in",
                "Life and liberty information must be provided within 48 hours"
            ],
            "keywords": ["RTI", "right to information", "transparency", "government", "public authority", "PIO", "information commission", "accountability"],
            "related": ["article-19", "article-21"]
        }
    ]
}


def get_all_legal_entries():
    """Flatten the knowledge base into a single list of all legal entries."""
    entries = []

    # Constitution
    for entry in LEGAL_KNOWLEDGE_BASE.get("constitution", []):
        entries.append(entry)

    # Criminal
    criminal = LEGAL_KNOWLEDGE_BASE.get("criminal", {})
    for entry in criminal.get("ipc", []):
        entries.append(entry)
    for entry in criminal.get("crpc", []):
        entries.append(entry)
    for entry in criminal.get("procedures", []):
        entries.append(entry)

    # Civil
    for entry in LEGAL_KNOWLEDGE_BASE.get("civil", []):
        entries.append(entry)

    # Family
    for entry in LEGAL_KNOWLEDGE_BASE.get("family", []):
        entries.append(entry)

    # Labor
    for entry in LEGAL_KNOWLEDGE_BASE.get("labor", []):
        entries.append(entry)

    # Consumer
    for entry in LEGAL_KNOWLEDGE_BASE.get("consumer", []):
        entries.append(entry)

    # Cyber
    for entry in LEGAL_KNOWLEDGE_BASE.get("cyber", []):
        entries.append(entry)

    # Rights
    for entry in LEGAL_KNOWLEDGE_BASE.get("rights", []):
        entries.append(entry)

    return entries


def get_entry_text(entry):
    """Convert a legal entry into a searchable text string."""
    parts = [
        entry.get("title", ""),
        entry.get("content", ""),
        entry.get("explanation", ""),
        " ".join(entry.get("keywords", [])),
        " ".join(entry.get("guidance", [])),
    ]
    if "steps" in entry:
        parts.append(" ".join(entry["steps"]))
    return " ".join(parts)
