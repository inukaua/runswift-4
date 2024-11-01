class_<RobotVisionInfo>("RobotVisionInfo")
   .def_readonly("rr"       , &RobotVisionInfo::rr      )
   .def_readonly("type"     , &RobotVisionInfo::type    )
   .def_readonly("imageCoords"     , &RobotVisionInfo::imageCoords   );

enum_<RobotVisionInfo::Type>("RobotVisionInfoType")
   .value("rUnknown"  , RobotVisionInfo::rUnknown    )
   .value("rBlue"     , RobotVisionInfo::rBlue       )
   .value("rRed"      , RobotVisionInfo::rRed        );

